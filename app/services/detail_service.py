"""Recipe detail service for fetching full recipe information."""

from typing import Optional

import pandas as pd

from app.models.recipe_detail import RecipeDetail
from app.core import config
from app.core.logging import get_logger

logger = get_logger(__name__)


class DetailService:
    """Service for retrieving detailed recipe information.
    
    Fetches full recipe data from master DataFrame and converts to RecipeDetail models.
    """

    def __init__(self, df: Optional[pd.DataFrame] = None):
        """Initialize with DataFrame containing recipe data.
        
        Args:
            df: DataFrame indexed by recipe_id, defaults to config.df
        """
        self.df = df if df is not None else getattr(config, "df", None)
        if self.df is None:
            logger.warning("DetailService initialized without DataFrame (config.df is None)")

    def get_recipe_details(self, recipe_id: int) -> Optional[RecipeDetail]:
        """Get complete recipe details by ID.
        
        Args:
            recipe_id: Recipe identifier
            
        Returns:
            RecipeDetail model with full recipe info, or None if not found
        """
        df = self.df
        if df is None:
            logger.debug("get_recipe_details: DataFrame is None")
            return None

        if recipe_id not in df.index:
            logger.debug("get_recipe_details: id %s not in index", recipe_id)
            return None

        row = df.loc[recipe_id]
        if isinstance(row, pd.DataFrame):
            if row.shape[0] == 0:
                return None
            row = row.iloc[0]

        row_dict = row.to_dict()
        try:
            row_dict["recipe_id"] = int(recipe_id)
        except Exception:
            row_dict["recipe_id"] = recipe_id
        
        row_dict.setdefault("keywords", [])
        row_dict.setdefault("ingredients", [])

        ri = row_dict.get("recipe_instructions")
        if ri is None:
            row_dict["recipe_instructions"] = []
        else:
            if isinstance(ri, str):
                row_dict["recipe_instructions"] = [s.strip() for s in ri.splitlines() if s.strip()]

        try:
            return RecipeDetail(**row_dict)
        except Exception as e:
            logger.exception("RecipeDetail validation failed for id=%s: %s", recipe_id, e)
            return None
