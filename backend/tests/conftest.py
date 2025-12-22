import pytest
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

from app import main as main_mod
from app.core import config


class FakeModel:
    def __init__(self, dim: int = 5):
        self.dim = dim
        # simple token map for deterministic behavior
        self.tokens = ["pasta", "pizza", "salad", "soup", "cake"][:dim]

    def _encode_one(self, text: str):
        vec = [0.0] * self.dim
        t = (text or "").lower()
        for i, tok in enumerate(self.tokens):
            if tok in t:
                vec[i] = 1.0
        if sum(vec) == 0:
            vec[0] = float(min(len(t), 10)) / 10.0
        return np.asarray(vec, dtype=np.float32)

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False, batch_size=None):
        if isinstance(texts, str):
            return self._encode_one(texts)
        return np.vstack([self._encode_one(t) for t in texts])


@pytest.fixture
def fake_model():
    return FakeModel(dim=5)


@pytest.fixture
def sample_embeddings():
    # small deterministic embeddings
    return np.array([[1.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0, 0.0]], dtype=np.float32)


@pytest.fixture
def sample_ids():
    return np.array([10, 11, 12], dtype=np.int64)


@pytest.fixture
def sample_df():
    df = pd.DataFrame({
        "recipe_id": [10, 11, 12],
        "name": ["A", "B", "C"],
        "keywords": [["k1"], "k2", None],
    })
    return df


@pytest.fixture
def client_with_preloaded_state(monkeypatch, sample_embeddings, sample_ids, fake_model, sample_df):
    config.embeddings = sample_embeddings
    config.ids = sample_ids
    config.model = fake_model
    config.df = sample_df.set_index("recipe_id", drop=False)

    config.temp_results = None

    client = TestClient(main_mod.app)
    return client