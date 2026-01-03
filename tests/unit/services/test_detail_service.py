"""Unit tests for DetailService."""

import pytest
import pandas as pd

from app.services.detail_service import DetailService
from app.models.recipe_detail import RecipeDetail


@pytest.fixture
def sample_df():
    """Create sample DataFrame with full recipe data."""
    df = pd.DataFrame([
        {
            "recipe_id": 1,
            "name": "Pasta Carbonara",
            "description": "Classic Italian pasta",
            "recipe_category": "Main Course",
            "keywords": ["pasta", "italian", "creamy"],
            "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "black pepper"],
            "recipe_instructions": ["Boil pasta", "Fry bacon", "Mix with eggs", "Add cheese"],
            "n_ingredients": 5,
            "total_time_minutes": 30,
            "calories": 450.5,
            "aggregated_rating": 4.7,
            "carbohydrate_content": 60.0,
            "fat_content": 15.0,
            "protein_content": 20.0,
            "sugar_content": 2.0,
            "carbohydrate_content_perc": 55.0,
            "fat_content_perc": 30.0,
            "protein_content_perc": 15.0,
            "sugar_content_perc": 5.0,
        },
        {
            "recipe_id": 2,
            "name": "Chicken Pizza",
            "description": "Delicious homemade pizza",
            "recipe_category": "Main Course",
            "keywords": ["pizza", "chicken", "cheese"],
            "ingredients": ["dough", "tomato sauce", "chicken", "mozzarella"],
            "recipe_instructions": ["Prepare dough", "Add toppings", "Bake"],
            "n_ingredients": 4,
            "total_time_minutes": 45,
            "calories": 680.0,
            "aggregated_rating": 4.5,
            "carbohydrate_content": 70.0,
            "fat_content": 25.0,
            "protein_content": 30.0,
            "sugar_content": 3.0,
            "carbohydrate_content_perc": 50.0,
            "fat_content_perc": 35.0,
            "protein_content_perc": 12.0,
            "sugar_content_perc": 3.0,
        },
    ])
    df = df.set_index("recipe_id")
    return df


class TestDetailService:
    """Tests for DetailService recipe detail retrieval."""

    def test_get_recipe_details_returns_recipe_detail(self, sample_df):
        """Should return RecipeDetail instance."""
        svc = DetailService(df=sample_df)
        detail = svc.get_recipe_details(1)
        assert detail is not None
        assert isinstance(detail, RecipeDetail)

    def test_get_recipe_details_has_all_fields(self, sample_df):
        """Should include all recipe fields."""
        svc = DetailService(df=sample_df)
        detail = svc.get_recipe_details(1)
        
        assert detail.recipe_id == 1
        assert detail.name == "Pasta Carbonara"
        assert detail.description == "Classic Italian pasta"
        assert detail.recipe_category == "Main Course"
        assert len(detail.ingredients) == 5
        assert len(detail.recipe_instructions) == 4
        assert len(detail.keywords) == 3
        assert detail.n_ingredients == 5
        assert detail.total_time_minutes == 30
        assert detail.calories == 450.5
        assert detail.aggregated_rating == 4.7

    def test_get_recipe_details_nutrition_fields(self, sample_df):
        """Should include nutrition information."""
        svc = DetailService(df=sample_df)
        detail = svc.get_recipe_details(1)
        
        assert detail.carbohydrate_content == 60.0
        assert detail.fat_content == 15.0
        assert detail.protein_content == 20.0
        assert detail.sugar_content == 2.0
        assert detail.carbohydrate_content_perc == 55.0
        assert detail.fat_content_perc == 30.0
        assert detail.protein_content_perc == 15.0
        assert detail.sugar_content_perc == 5.0

    def test_get_recipe_details_returns_none_for_missing_id(self, sample_df):
        """Should return None for non-existent recipe ID."""
        svc = DetailService(df=sample_df)
        detail = svc.get_recipe_details(999)
        assert detail is None

    def test_get_recipe_details_handles_none_dataframe(self):
        """Should return None when DataFrame is None."""
        svc = DetailService(df=None)
        detail = svc.get_recipe_details(1)
        assert detail is None

    def test_get_recipe_details_handles_empty_dataframe(self):
        """Should return None when DataFrame is empty."""
        svc = DetailService(df=pd.DataFrame())
        detail = svc.get_recipe_details(1)
        assert detail is None

    def test_get_recipe_details_handles_string_instructions(self, sample_df):
        """Should handle recipe_instructions as string and split by lines."""
        df = sample_df.copy()
        df.loc[1, 'recipe_instructions'] = "Step 1\nStep 2\nStep 3"
        
        svc = DetailService(df=df)
        detail = svc.get_recipe_details(1)
        
        assert isinstance(detail.recipe_instructions, list)
        assert len(detail.recipe_instructions) == 3
        assert "Step 1" in detail.recipe_instructions
