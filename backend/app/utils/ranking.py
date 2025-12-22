"""Ranking utilities for selecting top-k items from score arrays.

This module provides a compact, efficient top-k implementation using
NumPy's `argpartition` and is used by the search service to extract
the most similar recipes.
"""

import numpy as np
from typing import Tuple


def topk_from_pairs(ids: np.ndarray, scores: np.ndarray, k: int = 300) -> Tuple[np.ndarray, np.ndarray]:
    """Minimal top-k using `np.argpartition`. Caller provides valid inputs.

    Assumes `0 < k <= len(scores)`. If `k` exceeds available items, returns
    a fully-sorted list of all items in descending score order.
    """
    if scores is None or len(scores) == 0:
        return (np.array([], dtype=ids.dtype), np.array([], dtype=scores.dtype if scores is not None else float))

    n = len(scores)
    if k <= 0:
        return (np.array([], dtype=ids.dtype), np.array([], dtype=scores.dtype))

    # If requested k is larger than available items, just sort all
    k_effective = min(k, n)

    if k_effective == n:
        idx = np.argsort(-scores)
        return (ids[idx], scores[idx])

    part = np.argpartition(-scores, k_effective - 1)[:k_effective]
    idx = part[np.argsort(-scores[part])]
    return (ids[idx], scores[idx])