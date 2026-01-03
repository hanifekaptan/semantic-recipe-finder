

"""Vector store service using ChromaDB with DuckDB+Parquet backend.

This module provides:
- Global ChromaDB client initialization
- Collection loading/building from processed embeddings
- Semantic search functionality
"""

import os
import numpy as np
import chromadb
from chromadb.config import Settings
from typing import Tuple, List

from app.core.logging import get_logger

logger = get_logger(__name__)

# Constants
PERSIST_DIR = "data/processed/persist"
COLLECTION_NAME = "recipes"
IDS_EMBS_PATH = "data/processed/ids_embs.npy"
METADATA_EMBS_PATH = "data/processed/metadata_embs.npy"

# Global client instance
_client = None
_collection = None


def get_client():
    """Get or create global ChromaDB client with DuckDB+Parquet backend.
    
    Returns:
        chromadb.Client: Persistent ChromaDB client instance.
    """
    global _client
    
    if _client is None:
        logger.info(f"Initializing ChromaDB client with persist_dir={PERSIST_DIR}")
        
        # Ensure persist directory exists
        os.makedirs(PERSIST_DIR, exist_ok=True)
        
        # Create client with DuckDB+Parquet backend (persistent)
        _client = chromadb.PersistentClient(
            path=PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        logger.info("ChromaDB client initialized successfully")
    
    return _client


def load_or_build_collection():
    """Load existing collection or build new one from processed embeddings.
    
    Loads embeddings from:
    - data/processed/ids_embs.npy (recipe IDs)
    - data/processed/metadata_embs.npy (embedding vectors)
    
    Returns:
        chromadb.Collection: The recipes collection.
    """
    global _collection
    
    if _collection is not None:
        logger.info("Returning cached collection")
        return _collection
    
    client = get_client()
    
    try:
        # Try to get existing collection
        _collection = client.get_collection(name=COLLECTION_NAME)
        count = _collection.count()
        logger.info(f"Loaded existing collection '{COLLECTION_NAME}' with {count} items")
        
    except Exception as e:
        logger.info(f"Collection not found, building new one: {e}")
        
        # Load embeddings from disk
        if not os.path.exists(IDS_EMBS_PATH) or not os.path.exists(METADATA_EMBS_PATH):
            raise FileNotFoundError(
                f"Embedding files not found: {IDS_EMBS_PATH}, {METADATA_EMBS_PATH}"
            )
        
        logger.info(f"Loading embeddings from {IDS_EMBS_PATH} and {METADATA_EMBS_PATH}")
        ids_array = np.load(IDS_EMBS_PATH)
        embeddings_array = np.load(METADATA_EMBS_PATH)
        
        logger.info(f"Loaded {len(ids_array)} IDs and {embeddings_array.shape} embeddings")
        
        # Convert IDs to strings (ChromaDB requirement)
        ids_list = [str(int(id_)) for id_ in ids_array]
        embeddings_list = embeddings_array.tolist()
        
        # Create collection
        logger.info(f"Creating collection '{COLLECTION_NAME}'")
        _collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        # Add embeddings in batches (ChromaDB has limits)
        batch_size = 2000
        total = len(ids_list)
        
        for i in range(0, total, batch_size):
            end_idx = min(i + batch_size, total)
            batch_ids = ids_list[i:end_idx]
            batch_embeddings = embeddings_list[i:end_idx]
            
            logger.info(f"Adding batch {i//batch_size + 1}: items {i} to {end_idx}")
            _collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings
            )
        
        logger.info(f"Successfully built collection with {_collection.count()} items")
    
    return _collection


def search_collection(query_embedding: np.ndarray, top_k: int = 100) -> Tuple[List[int], List[float]]:
    """Search collection for most similar embeddings.
    
    Args:
        query_embedding: Query vector as numpy array (normalized).
        top_k: Number of results to return (default: 100).
    
    Returns:
        Tuple of (ids, distances):
            - ids: List of recipe IDs as integers
            - distances: List of similarity distances as floats
    """
    collection = load_or_build_collection()
    
    # Ensure query is normalized
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    
    # ChromaDB query
    results = collection.query(
        query_embeddings=[query_norm.tolist()],
        n_results=top_k
    )
    
    # Extract IDs and distances
    # results['ids'] is list of lists, results['distances'] is list of lists
    ids_str = results['ids'][0] if results['ids'] else []
    distances = results['distances'][0] if results['distances'] else []
    
    # Convert string IDs back to integers
    ids = [int(id_str) for id_str in ids_str]
    
    logger.info(f"Search returned {len(ids)} results")
    return ids, distances