import numpy as np
from app.utils.similarity_score_calculator import topk_chunked_similarity

def test_topk_chunked_basic():
    ids = np.array([1, 2, 3], dtype=np.int64)
    embs = np.array([[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]], dtype=np.float32)
    q = np.array([1.0, 0.0], dtype=np.float32)
    top_ids, top_sims = topk_chunked_similarity(ids, q, embs, k=2, chunk_size=2)
    assert len(top_ids) == 2
    assert len(top_sims) == 2
    assert top_sims[0] >= top_sims[1]  # descending order
