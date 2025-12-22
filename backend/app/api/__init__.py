"""API package aggregator.

This package exposes sub-routers used by the FastAPI application.
"""

from .health import router as health_router
from .search import router as search_router
