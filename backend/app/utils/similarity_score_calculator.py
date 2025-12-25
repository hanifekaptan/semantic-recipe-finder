"""Similarity utilities optimized for large (memmap) embeddings.

This module provides one primary helper:

- `topk_chunked_similarity(ids, query_vec, embeddings, k, chunk_size)` — a
  memory-friendly top-k selection that processes `embeddings` in chunks.

All functions expect NumPy arrays (memmap is accepted for `embeddings`).
Embeddings are assumed L2-normalized so dot-product equals cosine similarity.
"""

from typing import Tuple

import numpy as np


def topk_chunked_similarity(
    ids: np.ndarray,
    query_vec: np.ndarray,
    embeddings: np.ndarray,
    k: int = 100,
    chunk_size: int = 2000,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute top-k results using chunked dot-product processing.

    This function reads `embeddings` in blocks of `chunk_size` rows, finds
    top candidates inside each block (using `argpartition`), then performs a
    final selection over the collected candidates. It returns `(top_ids,
    top_sims)` sorted by descending similarity.

    Parameters
    - ids: 1-D array of int identifiers for each embedding
    - query_vec: 1-D array (same dimensionality as embeddings)
    - embeddings: 2-D array or memmap of shape (N, D)
    - k: number of top results to return
    - chunk_size: block size for streaming (tune to available RAM)
    """
    # Minimal runtime checks. Startup validation (data_loader) guarantees
    # embeddings and ids are consistent; avoid repeating expensive checks.
    if not isinstance(query_vec, np.ndarray):
        raise TypeError("query_vec must be a numpy.ndarray")
    if query_vec.ndim != 1:
        raise ValueError("query_vec must be 1-D")
    if embeddings.ndim != 2:
        raise ValueError("embeddings must be a 2-D array")
    if embeddings.shape[1] != query_vec.size:
        raise ValueError("query_vec dimensionality does not match embeddings")
    n = embeddings.shape[0]

    # Collect candidate ids and sims from each chunk
    cand_ids = []
    cand_sims = []

    for start in range(0, n, chunk_size):
        end = min(n, start + chunk_size)
        block = embeddings[start:end]
        sims = np.dot(block, query_vec).astype(np.float32)
        m = min(k, sims.size)
        if m <= 0:
            continue
        # indices of top-m within block (unsorted)
        idx = np.argpartition(-sims, m - 1)[:m]
        cand_ids.append(ids[start + idx])
        cand_sims.append(sims[idx])

    if len(cand_sims) == 0:
        return (np.array([], dtype=np.int64), np.array([], dtype=np.float32))

    all_ids = np.concatenate(cand_ids)
    all_sims = np.concatenate(cand_sims)

    total = all_sims.size
    if total <= k:
        order = np.argsort(-all_sims)
        return all_ids[order].astype(np.int64), all_sims[order].astype(np.float32)

    sel = np.argpartition(-all_sims, k - 1)[:k]
    sel_order = np.argsort(-all_sims[sel])
    final_idx = sel[sel_order]
    top_ids = all_ids[final_idx].astype(np.int64)
    top_sims = all_sims[final_idx].astype(np.float32)
    return top_ids, top_sims
