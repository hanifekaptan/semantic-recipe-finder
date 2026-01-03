"""Search API endpoints for semantic recipe search.

Provides:
- POST /search: Semantic search with pagination (20 results per page)
- GET /recipe/{recipe_id}: Get detailed recipe information
"""

from fastapi import APIRouter, HTTPException, Request, Query
from typing import List

from app.models.search_query import SearchQuery
from app.models.search_response import SearchResponse, SearchResult
from app.core import config
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    query: SearchQuery,
    request: Request,
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return (max 100)"),
):
    """Semantic search endpoint with pagination.
    
    - Searches top 100 most similar recipes
    - Returns paginated results (default: 20 per page)
    - Each result includes RecipeCard with basic recipe information
    
    Args:
        query: Search query with text
        offset: Number of results to skip (for pagination)
        limit: Number of results to return (1-100, default 20)
    
    Returns:
        SearchResponse with paginated results and total count
    """
    logger.info("search request: query=\"%s\" offset=%d limit=%d", query.query, offset, limit)

    model = getattr(config, "model", None)
    chroma_col = getattr(config, "chroma_collection", None)
    df = getattr(config, "df", None)
    
    if model is None or chroma_col is None or df is None:
        logger.warning("search resources not initialized (model=%s, chroma=%s, df=%s)", 
                      bool(model), bool(chroma_col), bool(df))
        raise HTTPException(
            status_code=503, 
            detail="Search service not ready. Please try again in a moment.",
            headers={"Retry-After": "10"}
        )

    search_svc = getattr(config, "search_service", None)
    if search_svc is None:
        from app.services.search_service import SearchService
        search_svc = SearchService(model=model, chroma_collection=chroma_col)
        config.search_service = search_svc
        logger.info("SearchService instantiated")

    try:
        all_results = search_svc.search_results(query.query, top_k=100)
        logger.info("search completed: found %d results", len(all_results))
    except Exception as e:
        logger.exception("search execution failed: %s", e)
        raise HTTPException(status_code=500, detail="Search execution failed")

    total_count = len(all_results)
    paginated_results = all_results[offset : offset + limit]
    
    logger.info("returning %d results (offset=%d, limit=%d, total=%d)", 
               len(paginated_results), offset, limit, total_count)

    return SearchResponse(
        search_results=paginated_results,
        total_count=total_count,
        offset=offset,
        limit=limit
    )


@router.get("/recipe/{recipe_id}")
def get_recipe_detail(recipe_id: int, request: Request):
    """Get detailed information for a specific recipe.
    
    Args:
        recipe_id: Unique recipe identifier
        
    Returns:
        RecipeDetail with full recipe information including ingredients and instructions
    """
    logger.info("get_recipe_detail: id=%d", recipe_id)

    df = getattr(config, "df", None)
    if df is None:
        logger.error("DataFrame not loaded")
        raise HTTPException(status_code=500, detail="Recipe database not available")

    if recipe_id not in df.index:
        logger.debug("recipe id=%d not found in index", recipe_id)
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")

    detail_svc = getattr(config, "detail_service", None)
    if detail_svc is None:
        from app.services.detail_service import DetailService
        detail_svc = DetailService(df)
        config.detail_service = detail_svc

    details = detail_svc.get_recipe_details(recipe_id)
    if details is None:
        logger.warning("recipe id=%d exists but details could not be loaded", recipe_id)
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} details not available")

    logger.info("returning recipe details: id=%d name=%s", recipe_id, getattr(details, 'name', 'N/A'))
    return details