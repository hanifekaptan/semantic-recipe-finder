"""Search service: preprocess query, vectorize and query vectorstore.

This encapsulates the end-to-end search flow used by the API layer.

Flow:
1. Clean and vectorize query text
2. Search ChromaDB for top 100 most similar recipe IDs
3. Fetch recipe data from DataFrame and build RecipeCard models
4. Return SearchResult list with cards and similarity scores
"""

from typing import List, Tuple
import pandas as pd

from app.utils.data_preprocessor import clean_text
from app.utils.vectorizer import vectorize_text
from app.services.vectorstore import search_collection
from app.core import config
from app.core.logging import get_logger
from app.models.search_response import SearchResult
from app.models.recipe_card import RecipeCard

logger = get_logger(__name__)


class SearchService:
    """Encapsulates semantic search logic.

    Uses `config.model` and `config.df` by default but can accept
    explicit instances when constructed for testing.
    """

    def __init__(self, model=None, chroma_collection=None, df=None):
        """Initialize SearchService.
        
        Args:
            model: SentenceTransformer model for vectorization
            chroma_collection: (deprecated) ChromaDB collection - not used anymore
            df: DataFrame with recipe details
        """
        self.model = model if model is not None else getattr(config, "model", None)
        self.df = df if df is not None else getattr(config, "df", None)

    def search(self, query: str, top_k: int = 100) -> Tuple[List[int], List[float]]:
        """Run semantic search and return top_k recipe IDs with similarity scores.

        Steps:
        1. Clean query text
        2. Vectorize query with model
        3. Search ChromaDB for most similar embeddings
        
        Args:
            query: Search query text
            top_k: Number of results to return (default: 100)

        Returns:
            Tuple of (recipe_ids, similarity_distances)
        """
        logger.info("SearchService.search: query='%s' top_k=%d", query, top_k)
        
        if not query or not query.strip():
            logger.debug("Empty query provided")
            return [], []

        model = self.model or getattr(config, "model", None)
        if model is None:
            logger.error("Model not initialized")
            raise RuntimeError("Model not initialized")

        # Clean and vectorize query
        cleaned_query = clean_text(query)
        logger.debug("Cleaned query: '%s'", cleaned_query)
        
        query_vector = vectorize_text(cleaned_query, model, normalize=True)
        logger.debug("Query vectorized, shape: %s", query_vector.shape)

        # Search ChromaDB
        ids, distances = search_collection(query_vector, top_k=top_k)
        
        logger.info("Search completed: found %d results", len(ids))
        return ids, distances

    def get_recipe_cards(self, ids: List[int]) -> List[RecipeCard]:
        """Build RecipeCard instances from recipe IDs using DataFrame.
        
        Fetches recipe data from DataFrame and creates RecipeCard models
        containing basic recipe information for display in search results.
        
        Args:
            ids: List of recipe IDs to fetch
            
        Returns:
            List of RecipeCard instances (may be shorter than input if some IDs not found)
        """
        logger.info("get_recipe_cards: processing %d ids", len(ids))
        
        df = self.df if self.df is not None else getattr(config, "df", None)
        if df is None or df.empty:
            logger.warning("DataFrame not available")
            return []
        
        logger.debug("DataFrame shape: %s, index name: %s, sample index: %s", 
                    df.shape, df.index.name, df.index[:3].tolist())
        logger.debug("First 5 IDs to lookup: %s", ids[:5] if len(ids) >= 5 else ids)

        # Columns needed for RecipeCard
        recipe_card_cols = [
            "name",
            "description",
            "recipe_category",
            "keywords",
            "n_ingredients",
            "total_time_minutes",
            "calories",
            "aggregated_rating",
        ]

        cards: List[RecipeCard] = []
        
        for rid in ids:
            if rid not in df.index:
                logger.debug("Recipe ID %d not in DataFrame", rid)
                # Still create minimal card with just ID
                try:
                    cards.append(RecipeCard(recipe_id=rid))
                except Exception:
                    pass
                continue

            try:
                # Get row data
                row = df.loc[rid, recipe_card_cols]
                
                # Handle duplicate indices
                if isinstance(row, pd.DataFrame):
                    if row.empty:
                        cards.append(RecipeCard(recipe_id=rid))
                        continue
                    row = row.iloc[0]

                # Convert to dict and add recipe_id
                row_dict = row.to_dict()
                row_dict["recipe_id"] = int(rid)
                
                # Create RecipeCard
                cards.append(RecipeCard(**row_dict))
                
            except Exception as e:
                logger.debug("Failed to create card for ID %d: %s", rid, e)
                # Fallback: minimal card with just ID
                try:
                    cards.append(RecipeCard(recipe_id=rid))
                except Exception:
                    pass

        logger.info("Built %d cards from %d requested IDs", len(cards), len(ids))
        return cards

    def search_results(self, query: str, top_k: int = 100) -> List[SearchResult]:
        """Run full search pipeline and return SearchResult list with cards.
        
        This is the main method used by the API. It:
        1. Searches ChromaDB for top_k most similar recipes
        2. Fetches recipe data and builds RecipeCard models
        3. Combines IDs, scores, and cards into SearchResult objects
        
        Args:
            query: Search query text
            top_k: Number of results to return (default: 100)
            
        Returns:
            List of SearchResult objects, each containing:
                - recipe_id: Recipe ID
                - similarity_score: Similarity distance from ChromaDB
                - card: RecipeCard with recipe details
        """
        logger.info("search_results: query='%s' top_k=%d", query, top_k)
        
        # Step 1: Get top_k IDs and distances from ChromaDB
        ids, distances = self.search(query, top_k=top_k)
        
        if not ids:
            logger.info("No results found")
            return []
        
        # Step 2: Build RecipeCard objects for these IDs
        cards = self.get_recipe_cards(ids)
        
        # Step 3: Create lookup map
        card_map = {card.recipe_id: card for card in cards}
        
        # Step 4: Build SearchResult list
        results: List[SearchResult] = []
        for rid, distance in zip(ids, distances):
            card = card_map.get(rid)
            results.append(
                SearchResult(
                    recipe_id=rid,
                    similarity_score=float(distance),
                    card=card
                )
            )
        
        logger.info("Returning %d search results", len(results))
        return results
        
