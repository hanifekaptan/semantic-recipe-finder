"""Helpers to vectorize text using a SentenceTransformer model.

This module provides a thin wrapper that encodes text and ensures the
returned vector has type `float32` and is optionally L2-normalized.
"""

from sentence_transformers import SentenceTransformer
from typing import List, Optional, Union
import numpy as np


def vectorize_text(
    text: str,
    model: SentenceTransformer,
    normalize: bool = True,
) -> np.ndarray:
    """Encode `text` into a 1-D float32 vector using `model`.

    Args:
        text: input string to encode.
        model: a loaded SentenceTransformer instance.
        normalize: whether to L2-normalize the resulting vector.

    Returns:
        1-D NumPy array of dtype `float32`.
    """

    emb = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    emb = np.asarray(emb, dtype=np.float32).ravel()

    if normalize:
        n = np.linalg.norm(emb)
        if n > 0:
            emb = emb / n

    return emb
