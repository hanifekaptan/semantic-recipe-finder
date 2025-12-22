import numpy as np
from app.utils.ranking import topk_from_pairs

def test_topk_basic():
    ids = np.array([1,2,3], dtype=np.int64)
    scores = np.array([0.1,0.9,0.5], dtype=np.float32)
    ids_out, scores_out = topk_from_pairs(ids, scores, k=2)
    assert list(ids_out) == [2,3]
    assert list(scores_out) == [0.9,0.5]

def test_topk_empty_and_zero_k():
    ids = np.array([], dtype=np.int64)
    scores = np.array([], dtype=np.float32)
    ids_out, scores_out = topk_from_pairs(ids, scores, k=0)
    assert ids_out.size == 0
    assert scores_out.size == 0
