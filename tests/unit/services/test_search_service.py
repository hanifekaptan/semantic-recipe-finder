"""Unit tests for SearchService."""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch

from app.services.search_service import SearchService
from app.core import config


class FakeModel:
    """Mock model for testing without actual SentenceTransformer."""
    def encode(self, texts, **kwargs):
        """Return fake 384-dimensional embedding for each text."""
        if isinstance(texts, str):
            texts = [texts]
        # Always return array of embeddings, one per text
        embeddings = np.array([np.random.rand(384).astype(np.float32) for _ in texts])
        return embeddings


@pytest.fixture
def sample_df():
    """Create sample DataFrame with recipe data."""
    df = pd.DataFrame({
        "recipe_id": [1, 2, 3],
        "name": ["Pasta Carbonara", "Chicken Pizza", "Chocolate Cake"],
        "description": ["Creamy pasta", "Cheesy pizza", "Rich cake"],
        "recipe_category": ["Main", "Main", "Dessert"],
        "keywords": [["pasta", "italian"], ["pizza", "cheese"], ["cake", "chocolate"]],
        "n_ingredients": [5, 8, 6],
        "total_time_minutes": [30, 45, 60],
        "calories": [450.0, 800.0, 350.0],
        "aggregated_rating": [4.5, 4.7, 4.8],
    }).set_index("recipe_id")
    return df


def test_search_empty_query_returns_empty():
    """Empty query should return empty results."""
    svc = SearchService(model=FakeModel(), df=pd.DataFrame())
    ids, distances = svc.search("")
    assert ids == []
    assert distances == []


def test_search_whitespace_query_returns_empty():
    """Whitespace-only query should return empty results."""
    svc = SearchService(model=FakeModel(), df=pd.DataFrame())
    ids, distances = svc.search("   ")
    assert ids == []
    assert distances == []


def test_search_raises_when_no_model():
    """Should raise RuntimeError when model is not available."""
    # Ensure config.model is also None
    original_model = getattr(config, 'model', None)
    config.model = None
    try:
        svc = SearchService(model=None, df=pd.DataFrame())
        with pytest.raises(RuntimeError, match="Model not initialized"):
            svc.search("test query")
    finally:
        config.model = original_model


@patch('app.services.search_service.search_collection')
def test_search_returns_correct_types(mock_search_collection, sample_df):
    """Search should return lists of ints and floats."""
    mock_search_collection.return_value = ([1, 2], [0.85, 0.72])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    ids, distances = svc.search("pasta", top_k=2)
    
    assert isinstance(ids, list)
    assert isinstance(distances, list)
    assert all(isinstance(x, int) for x in ids)
    assert all(isinstance(x, float) for x in distances)
    assert ids == [1, 2]
    assert distances == [0.85, 0.72]


@patch('app.services.search_service.search_collection')
def test_search_calls_vectorstore_with_correct_params(mock_search_collection, sample_df):
    """Search should call vectorstore with normalized query embedding."""
    mock_search_collection.return_value = ([1], [0.9])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    svc.search("test query", top_k=50)
    
    mock_search_collection.assert_called_once()
    call_args = mock_search_collection.call_args
    query_vector = call_args[0][0]
    top_k = call_args[1]['top_k']
    
    assert isinstance(query_vector, np.ndarray)
    assert top_k == 50


def test_get_recipe_cards_returns_cards_for_valid_ids(sample_df):
    """Should return RecipeCard objects for existing IDs."""
    svc = SearchService(df=sample_df)
    cards = svc.get_recipe_cards([1, 2])
    
    assert len(cards) == 2
    assert cards[0].recipe_id == 1
    assert cards[0].name == "Pasta Carbonara"
    assert cards[1].recipe_id == 2
    assert cards[1].name == "Chicken Pizza"


def test_get_recipe_cards_handles_missing_ids(sample_df):
    """Should create minimal cards for missing IDs."""
    svc = SearchService(df=sample_df)
    cards = svc.get_recipe_cards([1, 999, 2])
    
    # Backend creates minimal cards with None fields for missing IDs
    assert len(cards) == 3
    assert cards[0].recipe_id == 1
    assert cards[0].name == "Pasta Carbonara"  # Valid card
    assert cards[1].recipe_id == 999
    assert cards[1].name is None  # Minimal card
    assert cards[2].recipe_id == 2
    assert cards[2].name == "Chicken Pizza"  # Valid card


def test_get_recipe_cards_preserves_order(sample_df):
    """Should preserve the order of requested IDs."""
    svc = SearchService(df=sample_df)
    cards = svc.get_recipe_cards([3, 1, 2])
    
    assert len(cards) == 3
    assert cards[0].recipe_id == 3
    assert cards[1].recipe_id == 1
    assert cards[2].recipe_id == 2


def test_get_recipe_cards_returns_empty_when_df_none():
    """Should return empty list when DataFrame is not available."""
    # Ensure config.df is also None so backend doesn't fall back to it
    original_df = getattr(config, 'df', None)
    config.df = None
    try:
        svc = SearchService(df=None)
        cards = svc.get_recipe_cards([1, 2, 3])
        assert cards == []
    finally:
        config.df = original_df


def test_get_recipe_cards_returns_empty_when_df_empty():
    """Should return empty list when DataFrame is empty."""
    svc = SearchService(df=pd.DataFrame())
    cards = svc.get_recipe_cards([1, 2, 3])
    assert cards == []


@patch('app.services.search_service.search_collection')
def test_search_results_returns_search_result_objects(mock_search_collection, sample_df):
    """search_results should return SearchResult objects with cards."""
    mock_search_collection.return_value = ([1, 2], [0.95, 0.82])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    results = svc.search_results("pasta", top_k=2)
    
    assert len(results) == 2
    assert results[0].recipe_id == 1
    assert results[0].similarity_score == 0.95
    assert results[0].card is not None
    assert results[0].card.name == "Pasta Carbonara"
    assert results[1].recipe_id == 2
    assert results[1].similarity_score == 0.82


@patch('app.services.search_service.search_collection')
def test_search_results_returns_empty_for_no_results(mock_search_collection, sample_df):
    """search_results should return empty list when no results found."""
    mock_search_collection.return_value = ([], [])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    results = svc.search_results("nonexistent", top_k=100)
    
    assert results == []


@patch('app.services.search_service.search_collection')
def test_search_results_handles_partial_cards(mock_search_collection, sample_df):
    """search_results should handle cases where some IDs don't have cards."""
    mock_search_collection.return_value = ([1, 999, 2], [0.9, 0.8, 0.7])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    results = svc.search_results("test", top_k=3)
    
    assert len(results) == 3
    assert results[0].card is not None
    assert results[0].card.name == "Pasta Carbonara"
    # Backend creates minimal card (not None) for missing IDs
    assert results[1].card is not None
    assert results[1].card.recipe_id == 999
    assert results[1].card.name is None  # Minimal card with None fields
    assert results[2].card is not None
    assert results[2].card.name == "Chicken Pizza"


@patch('app.services.search_service.clean_text')
@patch('app.services.search_service.search_collection')
def test_search_calls_text_preprocessing(mock_search_collection, mock_clean_text, sample_df):
    """Search should preprocess query text before vectorization."""
    mock_clean_text.return_value = "cleaned query"
    mock_search_collection.return_value = ([1], [0.9])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    svc.search("RAW Query!!! 123", top_k=10)
    
    mock_clean_text.assert_called_once_with("RAW Query!!! 123")


@patch('app.services.search_service.vectorize_text')
@patch('app.services.search_service.search_collection')
def test_search_normalizes_query_embedding(mock_search_collection, mock_vectorize, sample_df):
    """Search should normalize query embedding before searching."""
    mock_vectorize.return_value = np.array([1.0, 0.0, 0.0, 0.0])
    mock_search_collection.return_value = ([1], [0.9])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    svc.search("test", top_k=10)
    
    # vectorize_text should be called with normalize=True
    mock_vectorize.assert_called_once()
    call_kwargs = mock_vectorize.call_args[1]
    assert call_kwargs.get('normalize') is True


def test_get_recipe_cards_handles_duplicate_indices():
    """Should handle DataFrame with duplicate recipe_id indices."""
    # Create DataFrame with duplicate indices
    df = pd.DataFrame({
        "recipe_id": [1, 1, 2],  # ID 1 appears twice
        "name": ["Pasta A", "Pasta B", "Pizza"],
        "description": ["desc1", "desc2", "desc3"],
        "recipe_category": ["Main", "Main", "Main"],
        "keywords": [["italian"], ["pasta"], ["pizza"]],
        "n_ingredients": [5, 6, 8],
        "total_time_minutes": [30, 35, 45],
        "calories": [450.0, 460.0, 800.0],
        "aggregated_rating": [4.5, 4.6, 4.7],
    }).set_index("recipe_id")
    
    svc = SearchService(df=df)
    cards = svc.get_recipe_cards([1, 2])
    
    # Should handle gracefully and return cards (taking first occurrence)
    assert len(cards) == 2
    assert cards[0].recipe_id == 1
    assert cards[1].recipe_id == 2


def test_get_recipe_cards_handles_none_optional_fields():
    """Should create minimal cards when DataFrame has None in complex fields."""
    # Backend's row.to_dict() + RecipeCard(**row_dict) pattern fails when some fields are None
    # This causes exception and fallback to minimal card
    df = pd.DataFrame({
        "recipe_id": [1, 2],
        "name": ["Pasta", "Pizza"],
        "description": [None, "Cheesy"],
        "recipe_category": ["Main", None],
        "keywords": [["italian"], ["cheese"]],  
        "n_ingredients": [5, None],
        "total_time_minutes": [None, 45],
        "calories": [450.0, None],
        "aggregated_rating": [None, 4.7],
    }).set_index("recipe_id")
    
    svc = SearchService(df=df)
    cards = svc.get_recipe_cards([1, 2])
    
    # Backend creates minimal cards when row.to_dict() or RecipeCard(**row_dict) fails
    assert len(cards) == 2
    assert cards[0].recipe_id == 1
    # Backend falls back to minimal card (all fields None except recipe_id)
    assert cards[0].name is None  
    assert cards[1].recipe_id == 2
    assert cards[1].name is None


def test_get_recipe_cards_handles_missing_columns():
    """Should handle DataFrame missing required card columns."""
    # DataFrame missing recipe_card_cols will cause KeyError in df.loc
    # Backend expects all columns to exist, creates minimal card on error
    df = pd.DataFrame({
        "recipe_id": [1],
        "name": ["Pasta"],
        # Missing required columns for RecipeCard
    }).set_index("recipe_id")
    
    svc = SearchService(df=df)
    cards = svc.get_recipe_cards([1])
    
    # Backend creates minimal card when columns missing (fallback in except)
    assert len(cards) == 1
    assert cards[0].recipe_id == 1
    # name will be None because df.loc[rid, recipe_card_cols] fails
    assert cards[0].name is None


@patch('app.services.search_service.search_collection')
def test_search_handles_vectorstore_error(mock_search_collection, sample_df):
    """Should handle errors from vectorstore gracefully."""
    mock_search_collection.side_effect = Exception("ChromaDB connection error")
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    
    # Should raise the exception (caller should handle)
    with pytest.raises(Exception, match="ChromaDB connection error"):
        svc.search("pasta", top_k=10)


def test_get_recipe_cards_handles_empty_id_list(sample_df):
    """Should return empty list for empty ID list."""
    svc = SearchService(df=sample_df)
    cards = svc.get_recipe_cards([])
    assert cards == []


@patch('app.services.search_service.search_collection')
def test_search_with_large_top_k(mock_search_collection, sample_df):
    """Should handle large top_k values correctly."""
    # Return fewer results than requested
    mock_search_collection.return_value = ([1, 2], [0.9, 0.8])
    
    svc = SearchService(model=FakeModel(), df=sample_df)
    ids, distances = svc.search("test", top_k=1000)
    
    # Should return actual results, not fail
    assert len(ids) == 2
    assert len(distances) == 2
    mock_search_collection.assert_called_once()
    assert mock_search_collection.call_args[1]['top_k'] == 1000
