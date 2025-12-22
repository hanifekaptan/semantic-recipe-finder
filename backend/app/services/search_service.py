"""Search service implementation.

Provides `SearchService` which encapsulates preprocessing, vectorization,
scoring and top-k selection. The class is lightweight and performs no
file I/O; it assumes embeddings/ids/model are provided at construction.
"""

import numpy as np
from typing import Any, Tuple

from app.utils.vectorizer import vectorize_text
from app.utils.data_preprocessor import clean_text
from app.utils.ranking import topk_from_pairs
from app.utils.similarity_score_calculator import calculate_cosine_similarity


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

	def score(self, query_vec: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
		ids, sims = calculate_cosine_similarity(self.ids, query_vec, self.embeddings)
		return ids, sims

	def topk(self, ids: np.ndarray, sims: np.ndarray, k: int = 300) -> Tuple[np.ndarray, np.ndarray]:
		return topk_from_pairs(ids, sims, k)

	def search(self, text: str, k: int = 300) -> Tuple[np.ndarray, np.ndarray]:
		processed = self.preprocess(text)
		vector = self.vectorize(processed)
		ids, sims = self.score(vector)
		return self.topk(ids, sims, k)

