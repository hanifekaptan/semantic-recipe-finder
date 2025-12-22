"""Health-check router for monitoring and readiness probes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Simple liveness endpoint used by orchestration and tests."""
    return {"status": "ok"}
