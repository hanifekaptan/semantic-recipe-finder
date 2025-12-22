import numpy as np
from app.utils.vectorizer import vectorize_text

def test_vectorize_uses_model(fake_model):
    q = "test"
    emb = vectorize_text(q, model=fake_model, normalize=False)
    assert isinstance(emb, np.ndarray)
    assert emb.size == fake_model.dim

def test_vectorizer_batch(fake_model):
    texts = ["a","bb","ccc"]
    emb = np.vstack([vectorize_text(t, model=fake_model, normalize=False) for t in texts])
    assert emb.shape[0] == 3
    assert emb.shape[1] == fake_model.dim
