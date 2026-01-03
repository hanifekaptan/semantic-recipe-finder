"""Backend API client for recipe search and detail retrieval."""

import requests

DEFAULT_BASE = "http://localhost:8000"


def search(query, offset=0, limit=10, base_url=DEFAULT_BASE, timeout=10):
    """Search recipes by semantic query.
    
    Args:
        query: Search query text
        offset: Number of results to skip for pagination
        limit: Maximum number of results to return
        base_url: API base URL
        timeout: Request timeout in seconds
        
    Returns:
        Search response dict with results, or None on error
    """
    try:
        res = requests.post(f"{base_url}/search?offset={offset}&limit={limit}", json={"query": query}, timeout=timeout)
        res.raise_for_status()
        return res.json()
    except Exception:
        return None


def get_recipe(recipe_id, base_url=DEFAULT_BASE, timeout=8):
    """
    Get recipe details by ID.
    
    Args:
        recipe_id: Recipe identifier
        base_url: API base URL
        timeout: Request timeout in seconds
        
    Returns:
        Recipe detail dict, or None on error
    """
    try:
        res = requests.get(f"{base_url}/recipe/{recipe_id}", timeout=timeout)
        res.raise_for_status()
        return res.json()
    except Exception:
        return None
