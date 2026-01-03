"""Main API router that aggregates all sub-routers."""

from fastapi import APIRouter

from app.api.search import router as search_router
from app.api.health import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(search_router)
