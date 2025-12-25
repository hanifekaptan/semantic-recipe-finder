from fastapi import APIRouter, HTTPException, Request, Query
from typing import List, Optional

from app.models.search_query import SearchQuery
from app.models.search_response import SearchResponse, SearchResult
from app.core import config

from app.services.search_service import SearchService
from app.services.recipe_service import RecipeService

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    query: SearchQuery,
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
):
    """Handle semantic search requests.

    The endpoint uses startup-loaded resources available on `app.core.config`.
    It builds lightweight search result cards via `RecipeService` and stores
    transient cards in `config.temp_results` for short-lived inspection.
    """

    embs = getattr(config, "embeddings", None)
    ids = getattr(config, "ids", None)
    model = getattr(config, "model", None)

    if embs is None or ids is None or model is None:
        # Resources not yet initialized (background init still running).
        # Return 503 Service Unavailable so clients can retry later. Include
        # a Retry-After header to suggest a wait time.
        raise HTTPException(
            status_code=503,
            detail="Search resources not initialized; warming up",
            headers={"Retry-After": "30"},
        )

    search_svc: Optional[SearchService] = getattr(config, "search_service", None)
    if search_svc is None:
        search_svc = SearchService(embs, ids, model, normalize_embeddings=False)

    if getattr(config, "temp_search_query", None) == query.query and getattr(config, "temp_search_pairs", None) is not None:
        pairs = config.temp_search_pairs
    else:
        k_needed = offset + limit
        max_k = min(max(k_needed, 300), 1000)
        ids_results, sims_results = search_svc.search(query.query, k=max_k)

        try:
            pairs = [(int(rid), float(score)) for rid, score in zip(ids_results.tolist(), sims_results.tolist())]
        except Exception:
            pairs = [(int(rid), float(score)) for rid, score in zip(ids_results, sims_results)]
        config.temp_search_pairs = pairs
        config.temp_search_query = query.query

    recipe_svc: Optional[RecipeService] = getattr(config, "recipe_service", None)
    if recipe_svc is None:
        df = getattr(config, "df", None)
        if df is not None:
            recipe_svc = RecipeService(df)

    try:
        cards = recipe_svc.get_cards_for_ids(ids_results, sims_results) if recipe_svc is not None else []
    except Exception:
        cards = []

    config.temp_results = cards

    total = len(pairs)
    start = offset
    end = start + limit

    sliced = pairs[start:end]

    results: List[SearchResult] = [
        SearchResult(recipe_id=int(rid), similarity_score=float(score))
        for rid, score in sliced
    ]

    return SearchResponse(
        search_results=results,
        total_count=total,
        offset=offset,
        limit=limit,
    )


@router.get("/recipe/{recipe_id}")
def get_recipe_detail(recipe_id: int, request: Request):
    """Return detailed recipe information for `recipe_id`."""
    
    df = getattr(config, "df", None)
    if df is None:
        raise HTTPException(status_code=500, detail="DataFrame not loaded")
    
    if recipe_id not in df.index:
        available_ids = df.index.tolist()[:10]
        raise HTTPException(
            status_code=404, 
            detail=f"Recipe {recipe_id} not in index. Sample IDs: {available_ids}"
        )
    
    recipe_svc: Optional[RecipeService] = getattr(config, "recipe_service", None)
    if recipe_svc is None:
        recipe_svc = RecipeService(df)

    details = recipe_svc.get_recipe_details(recipe_id)
    
    if details is None:
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")
    return details