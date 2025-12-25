"""Search service implementation.

Provides `SearchService` which encapsulates preprocessing, vectorization,
scoring and top-k selection. The class is lightweight and performs no
file I/O; it assumes embeddings/ids/model are provided at construction.
"""

import numpy as np
from typing import Any, Tuple

from app.utils.vectorizer import vectorize_text
from app.utils.data_preprocessor import clean_text
from app.utils.similarity_score_calculator import topk_chunked_similarity


class SearchService:
	"""Search service that assumes embeddings/ids/model are provided at startup.

	Usage pattern (recommended at app startup):
		embs = np.load(..., mmap_mode='r')  # float32 L2-normalized
		ids = np.load(...)
		model = SentenceTransformer(...)
		svc = SearchService(embs, ids, model, normalize_embeddings=False)

	Methods are lightweight and do not perform file I/O.
	"""

	def __init__(
		self,
		embeddings: np.ndarray,
		ids: np.ndarray,
		model: Any,
		normalize_embeddings: bool = True,
	) -> None:
		self.embeddings = embeddings
		self.ids = ids
		self.model = model
		self.normalize_embeddings = normalize_embeddings

	def preprocess(self, text: str) -> str:
		return clean_text(text)

	def vectorize(self, text: str) -> np.ndarray:
		return vectorize_text(text, self.model, normalize=True)

	def search(self, text: str, k: int = 300, chunk_size: int = 2000) -> Tuple[np.ndarray, np.ndarray]:
		processed = self.preprocess(text)
		vector = self.vectorize(processed)
		top_ids, top_sims = topk_chunked_similarity(self.ids, vector, self.embeddings, k=k, chunk_size=chunk_size)
		return top_ids, top_sims

