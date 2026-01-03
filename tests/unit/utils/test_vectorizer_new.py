"""Unit tests for text vectorization utilities."""

import pytest
import numpy as np
from app.utils.vectorizer import vectorize_text


class MockModel:
    """Mock SentenceTransformer model for testing."""
    
    def encode(self, texts):
        """Return fixed embeddings."""
        return np.array([[1.0, 0.0, 0.0]])


class MockCallableModel:
    """Mock callable model for testing."""
    
    def __call__(self, texts):
        """Return fixed embeddings."""
        return np.array([[0.5, 0.5, 0.0]])


def test_vectorize_with_model_encode():
    """Should use model.encode() method."""
    vec = vectorize_text("test", MockModel(), normalize=False)
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (3,)
    assert vec[0] == 1.0


def test_vectorize_with_callable():
    """Should work with callable model."""
    vec = vectorize_text("test", MockCallableModel(), normalize=False)
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (3,)
    assert vec[0] == 0.5


def test_vectorize_normalize_true():
    """Should normalize vector to unit length."""
    vec = vectorize_text("test", MockModel(), normalize=True)
    norm = np.linalg.norm(vec)
    assert np.isclose(norm, 1.0)


def test_vectorize_normalize_false():
    """Should not normalize when normalize=False."""
    vec = vectorize_text("test", MockModel(), normalize=False)
    assert vec[0] == 1.0
    assert vec[1] == 0.0


def test_vectorize_raises_on_none_model():
    """Should raise RuntimeError when model is None."""
    with pytest.raises(RuntimeError, match="No model provided"):
        vectorize_text("test", None)


def test_vectorize_raises_on_unsupported_model():
    """Should raise RuntimeError for unsupported model type."""
    # Use an object without encode() or __call__() methods
    unsupported_model = {"not": "a_model"}
    with pytest.raises(RuntimeError, match="Unsupported model type"):
        vectorize_text("test", unsupported_model)


def test_vectorize_returns_float_array():
    """Should return numpy array with float dtype."""
    vec = vectorize_text("test", MockModel())
    assert vec.dtype == np.float64 or vec.dtype == np.float32
