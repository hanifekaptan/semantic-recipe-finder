"""Detailed recipe model used by the API and frontend detail view."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RecipeDetail(BaseModel):
    recipe_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    recipe_category: Optional[str] = None
    ingredients: List[str] = Field(default_factory=list)
    recipe_instructions: Optional[List[str]] = Field(default_factory=list)
    keywords: Optional[List[str]] = Field(default_factory=list)
    n_ingredients: Optional[int] = None
    total_time_minutes: Optional[int] = None
    calories: Optional[float] = None
    aggregated_rating: Optional[float] = None
    carbohydrate_content: Optional[float] = None
    fat_content: Optional[float] = None
    protein_content: Optional[float] = None
    sugar_content: Optional[float] = None
    carbohydrate_content_perc: Optional[float] = None
    fat_content_perc: Optional[float] = None
    protein_content_perc: Optional[float] = None
    sugar_content_perc: Optional[float] = None