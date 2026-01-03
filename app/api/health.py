"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """Simple health check that returns service status.
    
    Returns:
        dict: Status object indicating service is operational
    """
    return {"status": "ok"}
