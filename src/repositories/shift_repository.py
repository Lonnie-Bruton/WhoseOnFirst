"""
Shift repository for database operations.

Handles all database operations related to shift configurations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .base_repository import BaseRepository
from ..models.shift import Shift


class ShiftRepository(BaseRepository[Shift]):
    """
    Repository for shift configuration database operations.

    Extends BaseRepository with shift-specific queries:
    - Get by shift number
    - Get weekend shifts
    - Get shifts by duration
    - Check shift number uniqueness

    Attributes:
        db: SQLAlchemy database session
    """

    def __init__(self, db: Session):
        """
        Initialize ShiftRepository.

        Args:
            db: SQLAlchemy database session
        """
        super().__init__(db, Shift)

    def get_by_shift_number(self, shift_number: int) -> Optional[Shift]:
        """
        Get shift by its shift number.

        Args:
            shift_number: The shift number (1-6 for standard Mon-Sun pattern)

        Returns:
            Shift instance if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            return (
                self.db.query(self.model)
                .filter(self.model.shift_number == shift_number)
                .first()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting shift by number: {str(e)}")

    def get_all_ordered(self) -> List[Shift]:
        """
        Get all shifts ordered by shift number.

        Returns:
            List of all shifts in sequential order

        Raises:
            Exception: If database operation fails
        """
        try:
            return (
                self.db.query(self.model)
                .order_by(self.model.shift_number)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting ordered shifts: {str(e)}")

    def get_weekend_shifts(self) -> List[Shift]:
        """
        Get all weekend shifts (Saturday and Sunday).

        Returns:
            List of weekend Shift instances

        Raises:
            Exception: If database operation fails
        """
        try:
            return (
                self.db.query(self.model)
                .filter(
                    (self.model.day_of_week.ilike('%saturday%')) |
                    (self.model.day_of_week.ilike('%sunday%'))
                )
                .order_by(self.model.shift_number)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting weekend shifts: {str(e)}")

    def get_by_duration(self, duration_hours: int) -> List[Shift]:
        """
        Get all shifts with a specific duration.

        Args:
            duration_hours: Duration to filter by (24 or 48)

        Returns:
            List of shifts with the specified duration

        Raises:
            Exception: If database operation fails
        """
        try:
            return (
                self.db.query(self.model)
                .filter(self.model.duration_hours == duration_hours)
                .order_by(self.model.shift_number)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting shifts by duration: {str(e)}")

    def shift_number_exists(self, shift_number: int, exclude_id: Optional[int] = None) -> bool:
        """
        Check if shift number already exists in database.

        Useful for validation before creating/updating shifts.

        Args:
            shift_number: Shift number to check
            exclude_id: Optional ID to exclude from check (for updates)

        Returns:
            True if shift number exists (and isn't the excluded ID), False otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            query = self.db.query(self.model).filter(
                self.model.shift_number == shift_number
            )

            if exclude_id is not None:
                query = query.filter(self.model.id != exclude_id)

            return query.count() > 0
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error checking shift number existence: {str(e)}")

    def get_by_day_of_week(self, day_of_week: str) -> List[Shift]:
        """
        Get shifts by day of week (case-insensitive partial match).

        Args:
            day_of_week: Day name to search for (e.g., "Monday", "Tuesday-Wednesday")

        Returns:
            List of matching Shift instances

        Raises:
            Exception: If database operation fails
        """
        try:
            search_term = f"%{day_of_week}%"
            return (
                self.db.query(self.model)
                .filter(self.model.day_of_week.ilike(search_term))
                .order_by(self.model.shift_number)
                .all()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting shifts by day: {str(e)}")

    def get_max_shift_number(self) -> int:
        """
        Get the highest shift number currently in use.

        Useful for determining the next shift number when adding new shifts.

        Returns:
            Maximum shift number, or 0 if no shifts exist

        Raises:
            Exception: If database operation fails
        """
        try:
            result = self.db.query(self.model.shift_number).order_by(
                self.model.shift_number.desc()
            ).first()

            return result[0] if result else 0
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error getting max shift number: {str(e)}")
