"""
API test fixtures and configuration.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.api.dependencies import get_db


@pytest.fixture
def client(db_session: Session):
    """
    FastAPI test client with database session override.

    This fixture provides a TestClient for making HTTP requests to the API
    with the test database session injected.

    Args:
        db_session: Test database session (from conftest.py)

    Yields:
        TestClient: Configured test client
    """
    def override_get_db():
        """Override database dependency with test session."""
        try:
            yield db_session
        finally:
            pass  # Session cleanup handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency override
    app.dependency_overrides.clear()
