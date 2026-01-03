"""Resource loading utilities for startup initialization."""

from typing import Tuple, Optional
import os
import pandas as pd

from app.services.vectorstore import load_or_build_collection
from app.core.logging import get_logger

logger = get_logger(__name__)


def read_parquet(candidates):
    """Read parquet file and return DataFrame with recipe_id as index.
    
    Tries multiple candidate paths and uses pyarrow engine with fallback.
    Sets recipe_id column as the DataFrame index if present.
    
    Args:
        candidates: Single path string or list of paths to try
        
    Returns:
        DataFrame with recipes data, or None if no file could be read
    """
    if not candidates:
        return None
    if isinstance(candidates, (str, bytes)):
        candidates = [candidates]

    for c in candidates:
        if not c or not os.path.exists(c):
            continue
        try:
            df = pd.read_parquet(c, engine="pyarrow")
            if "recipe_id" in df.columns:
                df = df.set_index("recipe_id")
            logger.info("loaded recipes dataframe via pandas+pyarrow: %s", c)
            return df
        except Exception:
            try:
                df = pd.read_parquet(c)
                if "recipe_id" in df.columns:
                    df = df.set_index("recipe_id", drop=False)
                logger.info("loaded recipes dataframe via pandas fallback: %s", c)
                return df
            except Exception:
                logger.debug("could not read parquet %s", c)
    return None


def get_chroma(metadata_embeddings_path: str = None, recipe_ids_path: str = None, collection_name: str = "recipes", persist_dir: Optional[str] = None):
    """Load or build ChromaDB collection.
    
    Parameters are kept for backward compatibility but now ignored.
    Uses vectorstore module's constants for paths and collection name.
    
    Returns:
        ChromaDB collection instance, or None on error
    """
    try:
        logger.debug("loading ChromaDB collection from vectorstore module")
        return load_or_build_collection()
    except Exception:
        logger.exception("failed to load or build chroma collection")
        return None


def load_model(name: Optional[str]):
    """Load SentenceTransformer model for text embedding.
    
    Args:
        name: Model name (e.g., 'all-MiniLM-L6-v2')
        
    Returns:
        SentenceTransformer instance, or None if name not provided or loading fails
    """
    if not name:
        return None
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        logger.warning("sentence-transformers not available: %s; model loading skipped", e)
        return None
    except Exception:
        logger.exception("unexpected error importing sentence-transformers")
        return None

    try:
        return SentenceTransformer(name)
    except Exception:
        logger.exception("failed to instantiate SentenceTransformer for %s", name)
        return None


def load_startup_resources(metadata_embeddings_path: str, recipe_ids_path: str, model_name: Optional[str], recipes_details_path: str) -> Tuple[Optional[object], Optional[pd.DataFrame], Optional[object], Optional[str]]:
    """Load model, dataframe and chroma collection for startup.

    Uses the top-level helpers in this module: `read_parquet`, `get_chroma`,
    and `load_model`. Returns (model, df, chroma_collection, error_msg).
    """
    err = None
    model = None
    df = None
    chroma_col = None

    # Read recipes details
    try:
        df = read_parquet(recipes_details_path)
    except Exception as e:
        logger.exception("failed to read recipes details: %s", recipes_details_path)
        err = f"failed to read recipes details: {e}"

    # Load model
    try:
        model = load_model(model_name)
    except Exception as e:
        logger.exception("failed to load model: %s", model_name)
        err = err or f"failed to load model: {e}"

    # Load or build chroma collection
    try:
        chroma_col = get_chroma(metadata_embeddings_path, recipe_ids_path)
    except Exception as e:
        logger.exception("failed to get chroma collection")
        err = err or f"failed to get chroma collection: {e}"

    return model, df, chroma_col, err
