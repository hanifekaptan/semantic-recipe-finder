"""Search response models used by the API.

Defines `SearchResult` and `SearchResponse` which represent the
lightweight results returned by the `/search` endpoint.
"""

from typing import List, Optional
from pydantic import BaseModel
from app.models.recipe_card import RecipeCard


class SearchResult(BaseModel):
    recipe_id: int
    similarity_score: float
    card: Optional[RecipeCard] = None


class SearchResponse(BaseModel):
    """Response model for search and filter endpoints."""
    search_results: List[SearchResult]
    total_count: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
