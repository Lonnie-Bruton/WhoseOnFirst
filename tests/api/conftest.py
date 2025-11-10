"""
API test fixtures and configuration.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.api.dependencies import get_db
from src.api.routes.auth import require_auth, require_admin
from src.models.user import User, UserRole


@pytest.fixture
def mock_admin_user(db_session: Session):
    """
    Create a mock admin user for testing.

    Args:
        db_session: Test database session

    Returns:
        User: Mock admin user instance
    """
    from src.repositories.user_repository import UserRepository
    from src.auth.utils import hash_password

    repo = UserRepository(db_session)
    user_data = {
        "username": "test_admin",
        "password_hash": hash_password("test_password"),
        "role": UserRole.ADMIN,
        "is_active": True
    }
    user = repo.create(user_data)
    return user


@pytest.fixture
def client(db_session: Session, mock_admin_user: User):
    """
    FastAPI test client with database and authentication overrides.

    This fixture provides a TestClient for making HTTP requests to the API
    with both the test database session and authentication bypassed.

    All requests are authenticated as the mock admin user by default.

    Args:
        db_session: Test database session (from conftest.py)
        mock_admin_user: Mock admin user for authentication

    Yields:
        TestClient: Configured test client with auth bypass
    """
    def override_get_db():
        """Override database dependency with test session."""
        try:
            yield db_session
        finally:
            pass  # Session cleanup handled by db_session fixture

    def override_require_auth():
        """Override authentication requirement for tests."""
        return mock_admin_user

    def override_require_admin():
        """Override admin requirement for tests."""
        return mock_admin_user

    # Override dependencies
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_auth] = override_require_auth
    app.dependency_overrides[require_admin] = override_require_admin

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency overrides
    app.dependency_overrides.clear()
