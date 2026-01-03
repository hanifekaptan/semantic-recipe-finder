"""Text vectorization utilities using sentence-transformers."""

import numpy as np
from typing import Any


def vectorize_text(text: str, model: Any, normalize: bool = True):
    """Convert text to embedding vector using the provided model.
    
    Supports SentenceTransformer models or any callable that accepts
    a list of strings and returns embeddings.
    
    Args:
        text: Text to vectorize
        model: SentenceTransformer instance or callable
        normalize: Whether to normalize the resulting vector (L2 norm)
        
    Returns:
        numpy array of embedding vector
        
    Raises:
        RuntimeError: If model is None or unsupported type
    """
    if model is None:
        raise RuntimeError("No model provided for vectorization")

    if hasattr(model, "encode"):
        vec = model.encode([text])[0]
    elif callable(model):
        vec = model([text])[0]
    else:
        raise RuntimeError("Unsupported model type for vectorization")

    arr = np.array(vec, dtype=float)
    if normalize:
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
    return arr
