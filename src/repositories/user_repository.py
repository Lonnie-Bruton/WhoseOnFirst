"""
User Repository

Data access layer for User model operations.
Provides CRUD operations and authentication-related queries.
"""

from typing import Optional
from sqlalchemy.orm import Session

from src.models.user import User, UserRole
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model.

    Handles all database operations for user authentication and management.
    """

    def __init__(self, db: Session):
        """
        Initialize UserRepository.

        Args:
            db: Database session
        """
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_active_users(self) -> list[User]:
        """
        Get all active users.

        Returns:
            List of active users
        """
        return self.db.query(User).filter(User.is_active == True).all()

    def get_by_role(self, role: UserRole) -> list[User]:
        """
        Get all users with a specific role.

        Args:
            role: User role to filter by

        Returns:
            List of users with the specified role
        """
        return self.db.query(User).filter(User.role == role).all()

    def activate(self, user_id: int) -> Optional[User]:
        """
        Activate a user account.

        Args:
            user_id: ID of user to activate

        Returns:
            Updated user if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.is_active = True
            self.db.commit()
            self.db.refresh(user)
        return user

    def deactivate(self, user_id: int) -> Optional[User]:
        """
        Deactivate a user account.

        Args:
            user_id: ID of user to deactivate

        Returns:
            Updated user if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_password(self, user_id: int, password_hash: str) -> Optional[User]:
        """
        Update user password hash.

        Args:
            user_id: ID of user to update
            password_hash: New bcrypt password hash

        Returns:
            Updated user if found, None otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            user.password_hash = password_hash
            self.db.commit()
            self.db.refresh(user)
        return user
