import numpy as np
from app.utils.similarity_score_calculator import calculate_cosine_similarity

def test_similarity_basic():
    ids = np.array([1,2], dtype=np.int64)
    embs = np.array([[1.0,0.0],[0.0,1.0]], dtype=np.float32)
    q = np.array([1.0,0.0], dtype=np.float32)
    ids_out, sims = calculate_cosine_similarity(ids, q, embs)
    assert list(ids_out) == [1,2]
    assert sims[0] > sims[1]
