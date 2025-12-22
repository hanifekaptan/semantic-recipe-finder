"""Data loading helpers for embeddings, ids and metadata DataFrames.

Centralizes file-system checks and basic validation for startup resources.
Functions:
 - load_parquet(path) -> Optional[pd.DataFrame]
 - load_npy_memmap(emb_path, ids_path) -> (embs, ids)
 - load_startup_resources(...) -> (embs, ids, model, df, error_msg)

Place all I/O and basic validation here so the rest of the app can assume
resources are already validated/normalized.
"""

import os
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import pyarrow


def load_parquet(path: str) -> Optional[pd.DataFrame]:
    """Load a parquet file and ensure a consistent recipe-id index.

    If `RecipeId` or `recipe_id` columns are present this function will set
    the DataFrame index accordingly and return the DataFrame. Returns ``None``
    when the file does not exist or cannot be read.
    """
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_parquet(path, engine="pyarrow")
        if df is not None:
            if "recipe_id" in df.columns:
                df = df.set_index("recipe_id", drop=False)
                # Try to coerce index to integer (many lookups expect int index)
                try:
                    df.index = df.index.astype("int64")
                    df["recipe_id"] = df["recipe_id"].astype("int64")
                except Exception:
                    # If coercion fails, keep as-is but code will handle missing lookups gracefully
                    pass
            return df
    except Exception:
        return None


def load_npy_memmap(emb_path: str, ids_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Load embeddings and ids saved as .npy using memory-mapping.

    Validations performed:
    - files exist
    - types are numpy arrays
    - shapes are compatible (ids 1-D, embs 2-D, lengths match)
    - dtype conversions to ``int64`` (ids) and ``float32`` (embs) are attempted
    - embeddings contain finite values

    Returns ``(embs, ids)`` on success. Raises informative exceptions on error.
    """
    if not os.path.exists(emb_path):
        raise FileNotFoundError(f"embeddings file not found: {emb_path}")
    if not os.path.exists(ids_path):
        raise FileNotFoundError(f"ids file not found: {ids_path}")

    embs = np.load(emb_path, mmap_mode="r")
    ids = np.load(ids_path, mmap_mode="r")

    if not isinstance(ids, np.ndarray):
        raise TypeError("ids must be a numpy.ndarray")
    if not isinstance(embs, np.ndarray):
        raise TypeError("embeddings must be a numpy.ndarray")

    # basic shape/dtype validations and safe conversions
    if ids.ndim != 1:
        raise ValueError("ids must be a 1-D array")
    if embs.ndim != 2:
        raise ValueError("embeddings must be a 2-D array")
    if ids.shape[0] != embs.shape[0]:
        raise ValueError("length of ids must match number of embeddings")

    if ids.dtype != np.int64:
        try:
            ids = ids.astype(np.int64)
        except Exception:
            raise ValueError("ids could not be converted to int64")

    if embs.dtype != np.float32:
        try:
            embs = embs.astype(np.float32)
        except Exception:
            raise ValueError("embeddings could not be converted to float32")

    if not np.isfinite(embs).all():
        raise ValueError("embeddings contain NaN or Inf values")

    return embs, ids


def load_startup_resources(
    emb_path: str,
    ids_path: str,
    model_name: str,
    master_parquet_path: str,
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[object], Optional[pd.DataFrame], Optional[str]]:
    """Load all startup resources (embeddings, ids, model, dataframe).

    Returns a tuple: ``(embs, ids, model, df, error_msg)``. On success
    ``error_msg`` is ``None``. On any failure, the failed resource is set
    to ``None`` and ``error_msg`` contains a short description.
    """
    try:
        embs, ids = load_npy_memmap(emb_path, ids_path)
    except Exception as e:
        return None, None, None, None, f"embeddings/ids load error: {e}"

    try:
        # import locally to avoid heavy imports at module import time
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_name)
    except Exception as e:
        return embs, ids, None, None, f"model load error: {e}"

    try:
        df = load_parquet(master_parquet_path)
    except Exception as e:
        return embs, ids, model, None, f"parquet load error: {e}"

    return embs, ids, model, df, None
