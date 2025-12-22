"""API routes aggregator.

This module centralizes and exposes the application's sub-routers.
Keep this file minimal to make route composition explicit and easy to modify.
"""

from fastapi import APIRouter
from .health import router as health_router
from .search import router as search_router

router = APIRouter()

router.include_router(health_router)
router.include_router(search_router)

__all__ = ["router"]
