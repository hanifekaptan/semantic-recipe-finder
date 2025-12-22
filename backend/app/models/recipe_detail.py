"""Pydantic model for detailed recipe information.

This module defines `RecipeDetail`, the canonical API model used to
serialize detailed recipe records returned by `/recipe/{id}`.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
import re

class RecipeDetail(BaseModel):
    recipe_id: int
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    recipe_category: Optional[str] = Field(default=None)
    keywords: Optional[List[str]] = Field(default_factory=list)
    n_ingredients: Optional[int] = Field(default=None)
    total_time_minutes: Optional[int] = Field(default=None)
    calories: Optional[float] = Field(default=None)
    aggregated_rating: Optional[float] = Field(default=None)
    ingredients: Optional[List[str]] = Field(default_factory=list)
    recipe_instructions: Optional[str] = Field(default=None)
    similarity_score: Optional[float] = Field(default=None)
    fat_content: Optional[str] = Field(default=None)
    protein_content: Optional[str] = Field(default=None)
    sugar_content: Optional[str] = Field(default=None)
    carbohydrate_content: Optional[str] = Field(default=None)
    fat_content_perc: Optional[float] = Field(default=None)
    protein_content_perc: Optional[float] = Field(default=None)
    sugar_content_perc: Optional[float] = Field(default=None)
    carbohydrate_content_perc: Optional[float] = Field(default=None)