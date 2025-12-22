"""Similarity score utilities.

This module exposes a small function to compute cosine (dot-product)
similarities between a single query vector and a matrix of stored
embeddings. Inputs are expected to be NumPy arrays.
"""

import numpy as np
from typing import Tuple


def calculate_cosine_similarity(
    ids: np.ndarray,
    query_vec: np.ndarray,
    embeddings: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute dot-product similarity between a single query vector and many embeddings.

    Caller guarantees inputs are NumPy ndarrays. This function performs
    minimal type/shape checks and returns `(ids_int64, sims_float32)`.
    """
    
    if not isinstance(query_vec, np.ndarray):
        raise TypeError("query_vec must be a numpy.ndarray")

    if query_vec.ndim != 1:
        raise ValueError("query_vec must be 1-D")
    if embeddings.shape[1] != query_vec.size:
        raise ValueError("query_vec dimensionality does not match embeddings")
    
    sims = np.dot(embeddings, query_vec).astype(np.float32)

    return (ids, sims)