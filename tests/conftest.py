"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Create FastAPI test client for API integration tests.
    
    Returns:
        TestClient instance with application context
    """
    return TestClient(app)
