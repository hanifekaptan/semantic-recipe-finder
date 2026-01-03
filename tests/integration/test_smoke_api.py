"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import numpy as np
import pandas as pd

from app.main import app
from app.core import config


class MockModel:
    """Mock SentenceTransformer model for testing."""
    
    def __init__(self, dim: int = 384):
        self.dim = dim

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True):
        """Generate mock embeddings based on text content."""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        for text in texts:
            vec = np.random.rand(self.dim).astype(np.float32)
            t = (text or "").lower()
            
            if "pasta" in t:
                vec[0] = 0.9
            elif "pizza" in t:
                vec[1] = 0.9
            elif "cake" in t:
                vec[2] = 0.9
            
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
                
            embeddings.append(vec)
        
        result = np.vstack(embeddings) if len(embeddings) > 1 else embeddings[0]
        return result


class MockChromaCollection:
    """Mock ChromaDB collection for testing."""
    
    def query(self, query_embeddings, n_results=100, **kwargs):
        """Return mock search results."""
        return {
            "ids": [["10", "11", "12"]],
            "distances": [[0.15, 0.25, 0.35]]
        }
    
    def count(self):
        """Return mock collection count."""
        return 3


@pytest.fixture
def sample_recipes_df():
    """Create sample DataFrame with recipe data for testing."""
    df = pd.DataFrame({
        "recipe_id": [10, 11, 12],
        "name": ["Pasta Carbonara", "Margherita Pizza", "Chocolate Cake"],
        "description": ["Delicious creamy pasta", "Classic Italian pizza", "Rich chocolate dessert"],
        "recipe_category": ["Main Course", "Main Course", "Dessert"],
        "keywords": [
            ["pasta", "italian", "creamy"],
            ["pizza", "italian", "cheese"],
            ["cake", "chocolate", "dessert"]
        ],
        "n_ingredients": [5, 6, 8],
        "total_time_minutes": [30, 45, 60],
        "calories": [500.0, 700.0, 450.0],
        "aggregated_rating": [4.5, 4.7, 4.8],
        "ingredients": [
            ["spaghetti", "eggs", "bacon", "parmesan", "pepper"],
            ["dough", "tomato", "mozzarella", "basil", "olive oil", "salt"],
            ["flour", "sugar", "cocoa", "eggs", "butter", "milk", "vanilla", "baking powder"]
        ],
        "recipe_instructions": [
            ["Boil pasta", "Fry bacon", "Mix with eggs", "Serve hot"],
            ["Prepare dough", "Add sauce", "Add cheese", "Bake 15 min"],
            ["Mix dry ingredients", "Add wet ingredients", "Bake 30 min", "Let cool"]
        ],
        "fat_content": [15.0, 20.0, 25.0],
        "protein_content": [20.0, 18.0, 8.0],
        "sugar_content": [2.0, 3.0, 35.0],
        "carbohydrate_content": [60.0, 70.0, 55.0],
        "fat_content_perc": [30.0, 35.0, 45.0],
        "protein_content_perc": [15.0, 12.0, 8.0],
        "sugar_content_perc": [5.0, 3.0, 40.0],
        "carbohydrate_content_perc": [55.0, 50.0, 48.0],
    }).set_index("recipe_id")
    return df


@pytest.fixture
def test_client(sample_recipes_df):
    """Create test client with mocked dependencies."""
    # Mock search_collection to avoid real ChromaDB calls
    with patch('app.services.search_service.search_collection') as mock_search:
        # Setup mock to return recipe IDs and distances
        mock_search.return_value = ([10, 11, 12], [0.95, 0.88, 0.75])
        
        config.model = MockModel()
        config.df = sample_recipes_df
        config.chroma_collection = MockChromaCollection()
        config.ready = True
        
        from app.services.search_service import SearchService
        from app.services.detail_service import DetailService
        
        config.search_service = SearchService(
            model=config.model,
            chroma_collection=config.chroma_collection,
            df=config.df
        )
        config.detail_service = DetailService(df=config.df)
        
        client = TestClient(app)
        yield client


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_returns_200(self, test_client):
        """Health endpoint should return 200 status."""
        response = test_client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_ok_status(self, test_client):
        """Health endpoint should return ok status."""
        response = test_client.get("/health")
        data = response.json()
        assert data["status"] == "ok"


class TestRecipeDetailEndpoint:
    """Tests for recipe detail endpoint."""
    
    def test_get_recipe_detail_returns_200(self, test_client):
        """Recipe detail endpoint should return 200 for valid ID."""
        response = test_client.get("/recipe/10")
        assert response.status_code == 200
    
    def test_get_recipe_detail_returns_correct_data(self, test_client):
        """Recipe detail should contain correct recipe data."""
        response = test_client.get("/recipe/10")
        data = response.json()
        
        assert data["recipe_id"] == 10
        assert data["name"] == "Pasta Carbonara"
        assert data["recipe_category"] == "Main Course"
        assert data["n_ingredients"] == 5
        assert data["total_time_minutes"] == 30
        assert data["calories"] == 500.0
    
    def test_get_recipe_detail_includes_ingredients(self, test_client):
        """Recipe detail should include ingredients list."""
        response = test_client.get("/recipe/10")
        data = response.json()
        
        assert "ingredients" in data
        assert isinstance(data["ingredients"], list)
        assert len(data["ingredients"]) == 5
    
    def test_get_recipe_detail_includes_instructions(self, test_client):
        """Recipe detail should include recipe instructions."""
        response = test_client.get("/recipe/10")
        data = response.json()
        
        assert "recipe_instructions" in data
        assert isinstance(data["recipe_instructions"], list)
        assert len(data["recipe_instructions"]) == 4
    
    def test_get_recipe_detail_includes_nutrition(self, test_client):
        """Recipe detail should include nutrition information."""
        response = test_client.get("/recipe/10")
        data = response.json()
        
        assert "fat_content" in data
        assert "protein_content" in data
        assert "carbohydrate_content" in data
        assert "sugar_content" in data
    
    def test_get_recipe_detail_not_found(self, test_client):
        """Should return 404 for non-existent recipe ID."""
        response = test_client.get("/recipe/99999")
        assert response.status_code == 404


class TestSearchEndpoint:
    """Tests for search endpoint."""
    
    def test_search_returns_200(self, test_client):
        """Search endpoint should return 200 status."""
        response = test_client.post("/search", json={"query": "pasta"})
        assert response.status_code == 200
    
    def test_search_returns_correct_structure(self, test_client):
        """Search response should have correct structure."""
        response = test_client.post("/search", json={"query": "pasta"})
        data = response.json()
        
        assert "search_results" in data
        assert "total_count" in data
        assert "offset" in data
        assert "limit" in data
        assert isinstance(data["search_results"], list)
    
    def test_search_results_contain_cards(self, test_client):
        """Search results should contain recipe cards."""
        response = test_client.post("/search", json={"query": "pasta"})
        data = response.json()
        
        if len(data["search_results"]) > 0:
            result = data["search_results"][0]
            assert "recipe_id" in result
            assert "similarity_score" in result
            assert "card" in result
            
            if result["card"]:
                card = result["card"]
                assert "name" in card
                assert "description" in card
    
    def test_search_pagination_offset(self, test_client):
        """Search should support offset parameter."""
        response = test_client.post("/search?offset=1&limit=1", json={"query": "italian"})
        data = response.json()
        
        assert data["offset"] == 1
        assert data["limit"] == 1
    
    def test_search_pagination_limit(self, test_client):
        """Search should respect limit parameter."""
        response = test_client.post("/search?limit=2", json={"query": "italian"})
        data = response.json()
        
        assert len(data["search_results"]) <= 2
    
    def test_search_empty_query_returns_results(self, test_client):
        """Empty query should not cause server error."""
        response = test_client.post("/search", json={"query": ""})
        assert response.status_code in [200, 400]
    
    def test_search_missing_query_returns_422(self, test_client):
        """Missing query field should return 422 validation error."""
        response = test_client.post("/search", json={})
        assert response.status_code == 422
