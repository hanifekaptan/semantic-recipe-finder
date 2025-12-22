from typing import List, Any, Iterable, Optional
import pandas as pd

from app.models.recipe_detail import RecipeDetail
from app.core import config


class RecipeService:
    """Service providing recipe card and detail retrieval from a master DataFrame.

    The service expects a pandas DataFrame with recipe metadata. If no DataFrame
    is passed to the constructor, the service will use `app.core.config.df`.
    Methods are intentionally defensive: missing rows or corrupt entries are
    handled gracefully and minor inconsistencies (duplicate indices, missing
    keyword formats) are normalized.
    """

    def __init__(self, df: Optional[pd.DataFrame] = None):
        """Initialize the service with an optional DataFrame.

        Args:
            df: pandas DataFrame indexed by recipe id (optional). If omitted
                the service will read `config.df`.
        """
        self.df = df if df is not None else getattr(config, "df", None)

    def get_cards_for_ids(self, ids, sims) -> List[dict]:
        """Build lightweight card dictionaries for given ids and similarity scores.

        Args:
            ids: iterable of recipe ids (or values convertible to int).
            sims: iterable of similarity scores (or values convertible to float).

        Returns:
            List of dicts containing a subset of recipe fields and the
            similarity score. Missing or malformed rows are skipped.
        """
        ids_list = [int(x) for x in list(ids)]
        sims_list = [float(x) for x in list(sims)]

        df = self.df
        if df is None or df.shape[0] == 0:
            return []

        cards: List[dict] = []

        for rid, sim in zip(ids_list, sims_list):
            # Access each row individually to handle non-unique indices safely
            try:
                row = df.loc[rid]
            except KeyError:
                continue

            # If multiple rows match the id, pick the first
            if isinstance(row, pd.DataFrame):
                if row.shape[0] == 0:
                    continue
                row = row.iloc[0]

            # Skip rows where all non-identifier fields are null
            try:
                row_check = row.drop(labels=["recipe_id"], errors="ignore") if hasattr(row, "drop") else row
                isnull_func = getattr(row_check, "isnull", None)
                if callable(isnull_func):
                    isnull_res = isnull_func()
                    if getattr(isnull_res, "all", None) is not None and isnull_res.all():
                        continue
            except Exception:
                pass

            row_dict = row.to_dict()
            card = {
                "recipe_id": int(row_dict.get("recipe_id") or 0),
                "name": row_dict.get("name"),
                "description": row_dict.get("description"),
                "recipe_category": row_dict.get("recipe_category"),
                "keywords": row_dict.get("keywords"),
                "n_ingredients": row_dict.get("n_ingredients"),
                "total_time_minutes": row_dict.get("total_time_minutes"),
                "calories": row_dict.get("calories"),
                "aggregated_rating": row_dict.get("aggregated_rating"),
                "similarity_score": float(sim),
            }

            # Normalize Keywords: None -> [], string -> split by comma, keep list as-is
            kw = card.get("keywords")
            if kw is None:
                card["keywords"] = []
            elif isinstance(kw, str):
                card["keywords"] = [k.strip() for k in kw.split(",") if k.strip()]

            cards.append(card)

        return cards

    def get_recipe_details(self, recipe_id: int) -> Any:
        """Return a `RecipeDetail` pydantic model for given recipe id.

        Returns `None` if the recipe is missing or the row is malformed.
        """
        df = self.df
        if df is None:
            return None
        try:
            row = df.loc[recipe_id]
        except Exception:
            return None

        # If multiple rows match the id, reduce to the first row
        if isinstance(row, pd.DataFrame):
            if row.shape[0] == 0:
                return None
            row = row.iloc[0]

        # Skip if all non-identifier fields are null
        try:
            row_check = row.drop(labels=["recipe_id"], errors="ignore") if hasattr(row, "drop") else row
            isnull_func = getattr(row_check, "isnull", None)
            if callable(isnull_func):
                isnull_res = isnull_func()
                if getattr(isnull_res, "all", None) is not None and isnull_res.all():
                    return None
        except Exception:
            pass

        row_dict = row.to_dict()

        # Normalize keywords
        kw = row_dict.get("keywords")
        if kw is None:
            row_dict["keywords"] = []
        elif isinstance(kw, str):
            row_dict["keywords"] = [k.strip() for k in kw.split(",") if k.strip()]

        # Normalize ingredients
        ci = row_dict.get("ingredients")
        if ci is None:
            row_dict["ingredients"] = []
        elif isinstance(ci, str):
            row_dict["ingredients"] = [c.strip() for c in ci.split(",") if c.strip()]
        elif isinstance(ci, (list, tuple)):
            row_dict["ingredients"] = [str(x) for x in ci]

        # Normalize recipe_instructions: arrays/lists -> single string
        ri = row_dict.get("recipe_instructions")
        if ri is None:
            row_dict["recipe_instructions"] = None
        else:
            try:
                # handle numpy arrays or lists of strings
                if hasattr(ri, "tolist") and not isinstance(ri, str):
                    parts = list(ri.tolist())
                    row_dict["recipe_instructions"] = "\n".join([str(p).strip() for p in parts if str(p).strip()])
                elif isinstance(ri, (list, tuple)):
                    row_dict["recipe_instructions"] = "\n".join([str(p).strip() for p in ri if str(p).strip()])
                else:
                    row_dict["recipe_instructions"] = str(ri)
            except Exception:
                row_dict["recipe_instructions"] = str(ri)

        # Convert numeric nutrition fields to strings because RecipeDetail expects strings
        for nutr in ("fat_content", "protein_content", "sugar_content", "carbohydrate_content"):
            val = row_dict.get(nutr)
            if val is None:
                row_dict[nutr] = None
            else:
                # If numpy scalar or number, convert to python number then to string
                try:
                    if hasattr(val, "item") and not isinstance(val, (list, dict, str)):
                        val = val.item()
                except Exception:
                    pass
                # Now, if it's a number, format; otherwise cast to str
                if isinstance(val, (int, float)):
                    # keep reasonable precision
                    row_dict[nutr] = str(val)
                else:
                    row_dict[nutr] = str(val)

        # Convert numpy scalar types to native python types for pydantic (remaining fields)
        for k, v in list(row_dict.items()):
            try:
                if hasattr(v, "item") and not isinstance(v, (list, dict)):
                    row_dict[k] = v.item()
            except Exception:
                pass

        try:
            return RecipeDetail(**row_dict)
        except Exception as e:
            print(f"RecipeDetail validation failed for id={recipe_id}: {e}")
            return None