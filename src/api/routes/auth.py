"""
Authentication API Routes

Handles user login, logout, and session management.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from typing import Optional

from src.models.database import get_db
from src.api.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    UserResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    ResetViewerPasswordRequest,
    ResetViewerPasswordResponse
)
from src.auth.utils import (
    authenticate_user,
    create_session_cookie,
    get_current_user,
    hash_password,
    verify_password
)
from src.repositories.user_repository import UserRepository

router = APIRouter()


def get_session_user_id(session: Optional[str] = Cookie(default=None)) -> Optional[int]:
    """
    Get user ID from session cookie.

    Args:
        session: Session cookie value

    Returns:
        User ID if valid session, None otherwise
    """
    if not session:
        return None

    try:
        session_data = json.loads(session)
        return session_data.get("user_id")
    except (json.JSONDecodeError, KeyError):
        return None


def require_auth(
    session: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db)
):
    """
    Dependency to require authentication.

    Args:
        session: Session cookie
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If not authenticated
    """
    user_id = get_session_user_id(session)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return get_current_user(db, user_id)


def require_admin(current_user = Depends(require_auth)):
    """
    Dependency to require admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if admin

    Raises:
        HTTPException: If not admin
    """
    from src.models.user import UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and create session.

    Args:
        credentials: Login credentials (username, password, remember_me)
        response: Response object to set cookie
        db: Database session

    Returns:
        Login response with user info

    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create session data
    session_data = create_session_cookie(user.id, credentials.remember_me)

    # Set session cookie
    max_age = 2592000 if credentials.remember_me else 86400  # 30 days or 24 hours
    response.set_cookie(
        key="session",
        value=json.dumps(session_data),
        max_age=max_age,
        httponly=True,
        samesite="lax",  # Safe for same-origin (frontend and backend both on port 8000)
        secure=False,  # Set to True in production with HTTPS
        path="/"
    )

    return LoginResponse(
        username=user.username,
        role=user.role.value
    )


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing session cookie.

    Args:
        response: Response object to clear cookie

    Returns:
        Logout confirmation
    """
    response.delete_cookie(key="session")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(require_auth)):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user (from dependency)

    Returns:
        Current user information
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value,
        is_active=current_user.is_active
    )


@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.

    Args:
        request: Password change request (current and new password)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If current password is incorrect
    """
    # Verify current password
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    user_repo = UserRepository(db)
    new_hash = hash_password(request.new_password)
    user_repo.update_password(current_user.id, new_hash)

    return ChangePasswordResponse()


@router.post("/admin/reset-viewer-password", response_model=ResetViewerPasswordResponse)
async def reset_viewer_password(
    request: ResetViewerPasswordRequest,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Reset the viewer user's password (admin only).

    Args:
        request: Password reset request (new password)
        current_user: Current authenticated admin user
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If viewer user not found
    """
    # Get the viewer user
    user_repo = UserRepository(db)
    viewer_user = user_repo.get_by_username("viewer")

    if not viewer_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Viewer user not found"
        )

    # Update viewer password
    new_hash = hash_password(request.new_password)
    user_repo.update_password(viewer_user.id, new_hash)

    return ResetViewerPasswordResponse()
