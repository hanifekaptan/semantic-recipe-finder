"""Lightweight recipe card model used in search results.

`RecipeCard` contains a small subset of fields optimized for list
presentation (cards or search results).
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class RecipeCard(BaseModel):
    recipe_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    recipe_category: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list)
    n_ingredients: Optional[int] = None
    total_time_minutes: Optional[int] = None
    calories: Optional[float] = None
    aggregated_rating: Optional[float] = None
