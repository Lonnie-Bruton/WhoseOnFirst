"""
Rotation Algorithm Service

This module implements the circular rotation algorithm for assigning team members
to on-call shifts in a fair, predictable manner.

The algorithm works by:
1. Ordering team members consistently (by ID)
2. Ordering shifts by shift_number
3. Each week, rotating assignments forward by one position
4. Handling any team size (including cases where members < shifts or members > shifts)

Example with 7 members and 6 shifts:
- Week 1: Members 0-5 work shifts 1-6, member 6 is off
- Week 2: Members 1-6 work shifts 1-6, member 0 is off
- Week 3: Members 2-6,0 work shifts 1-6, member 1 is off

The double-shift (e.g., Tuesday-Wednesday 48h) naturally spreads across weeks,
ensuring no special "weekend fairness" logic is needed.
"""

from datetime import datetime, timedelta, time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from pytz import timezone

from src.repositories.team_member_repository import TeamMemberRepository
from src.repositories.shift_repository import ShiftRepository


class RotationAlgorithmError(Exception):
    """Base exception for rotation algorithm errors."""
    pass


class InsufficientMembersError(RotationAlgorithmError):
    """Raised when there are not enough active team members for rotation."""
    pass


class NoShiftsConfiguredError(RotationAlgorithmError):
    """Raised when no shifts are configured in the system."""
    pass


class InvalidWeekCountError(RotationAlgorithmError):
    """Raised when the week count is invalid (< 1)."""
    pass


class RotationAlgorithmService:
    """
    Service for generating fair on-call rotation schedules.

    This service implements a simple circular rotation algorithm where team members
    rotate through shifts in a predictable order each week. The rotation is fair
    because everyone moves forward by one position weekly, ensuring equal distribution
    of shifts over time.
    """

    # Mapping of day names to weekday offsets (Monday = 0)
    DAY_OFFSET_MAP = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    def __init__(self, db: Session):
        """
        Initialize the rotation algorithm service.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.team_member_repo = TeamMemberRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.chicago_tz = timezone('America/Chicago')

    def generate_rotation(
        self,
        start_date: datetime,
        weeks: int = 4,
        active_members_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate a fair rotation schedule for the specified number of weeks.

        This method creates schedule entries by rotating team members through
        shifts in a circular pattern. Each week, every member moves to the next
        shift in sequence (or is off duty if there are more members than shifts).

        Args:
            start_date: Start date for the rotation (timezone-aware).
                       Will be normalized to the Monday of that week.
            weeks: Number of weeks to generate (minimum 1, default 4)
            active_members_only: If True, only include active team members

        Returns:
            List of schedule entry dictionaries ready for ScheduleRepository.bulk_create().
            Each dict contains: team_member_id, shift_id, week_number,
            start_datetime, end_datetime, notified (False).

        Raises:
            InsufficientMembersError: If there are no active members available
            NoShiftsConfiguredError: If no shifts are configured
            InvalidWeekCountError: If weeks < 1
            ValueError: If start_date is not timezone-aware

        Example:
            >>> service = RotationAlgorithmService(db)
            >>> start = chicago_tz.localize(datetime(2025, 11, 4))
            >>> entries = service.generate_rotation(start, weeks=4)
            >>> len(entries)  # 7 members * 6 shifts * 4 weeks
            168
        """
        # Validate inputs
        self._validate_inputs(start_date, weeks)

        # Get team members (sorted by ID for consistency)
        members = self._get_team_members(active_members_only)
        if not members:
            raise InsufficientMembersError(
                "No active team members available for rotation"
            )

        # Get shifts (ordered by shift_number)
        shifts = self.shift_repo.get_all_ordered()
        if not shifts:
            raise NoShiftsConfiguredError(
                "No shifts configured. Please create shifts before generating rotation."
            )

        # Normalize start_date to Monday of that week
        monday = self._get_week_start(start_date)

        # Generate schedule entries
        schedule_entries = []

        for week in range(weeks):
            # Calculate the rotation offset for this week
            week_offset = week % len(members)

            # Assign members to shifts for this week
            for shift_index, shift in enumerate(shifts):
                # Circular rotation: each week, everyone moves forward one position
                member_index = (shift_index + week_offset) % len(members)
                member = members[member_index]

                # Calculate shift start datetime
                shift_start_datetime = self._calculate_shift_start(
                    monday, week, shift
                )

                # Calculate shift end datetime
                shift_end_datetime = shift_start_datetime + timedelta(
                    hours=shift.duration_hours
                )

                # Get ISO week number
                week_number = shift_start_datetime.isocalendar()[1]

                # Create schedule entry
                entry = {
                    "team_member_id": member.id,
                    "shift_id": shift.id,
                    "week_number": week_number,
                    "start_datetime": shift_start_datetime,
                    "end_datetime": shift_end_datetime,
                    "notified": False
                }

                schedule_entries.append(entry)

        return schedule_entries

    def _validate_inputs(self, start_date: datetime, weeks: int) -> None:
        """
        Validate input parameters.

        Args:
            start_date: The start date to validate
            weeks: The number of weeks to validate

        Raises:
            ValueError: If start_date is not timezone-aware
            InvalidWeekCountError: If weeks < 1
        """
        if start_date.tzinfo is None:
            raise ValueError(
                "start_date must be timezone-aware. "
                "Use chicago_tz.localize() or start_date.replace(tzinfo=...)"
            )

        if weeks < 1:
            raise InvalidWeekCountError(
                f"weeks must be >= 1, got {weeks}"
            )

    def _get_team_members(self, active_only: bool) -> List:
        """
        Get team members sorted by ID for consistent rotation order.

        Args:
            active_only: If True, only return active members

        Returns:
            List of TeamMember objects sorted by ID
        """
        if active_only:
            members = self.team_member_repo.get_active()
        else:
            members = self.team_member_repo.get_all()

        # Sort by ID for consistent, predictable rotation order
        return sorted(members, key=lambda m: m.id)

    def _get_week_start(self, date: datetime) -> datetime:
        """
        Normalize a date to the Monday of that week at midnight.

        Args:
            date: Any datetime in the target week

        Returns:
            Datetime representing Monday 00:00 of that week (timezone-aware)

        Example:
            >>> # Wednesday, Nov 6, 2025
            >>> wed = chicago_tz.localize(datetime(2025, 11, 6, 15, 30))
            >>> monday = self._get_week_start(wed)
            >>> monday  # Monday, Nov 4, 2025 00:00
        """
        # Monday = 0, Sunday = 6
        days_since_monday = date.weekday()

        # Go back to Monday, preserving timezone
        monday = date - timedelta(days=days_since_monday)

        # Set to midnight using replace() to keep timezone
        monday_midnight = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        return monday_midnight

    def _calculate_shift_start(
        self,
        base_monday: datetime,
        week: int,
        shift
    ) -> datetime:
        """
        Calculate the start datetime for a shift.

        Args:
            base_monday: The Monday of the first week (at midnight)
            week: Week offset (0 = first week, 1 = second week, etc.)
            shift: Shift object with day_of_week and duration_hours

        Returns:
            Timezone-aware datetime when the shift starts (8:00 AM Chicago time)

        Note:
            Shifts start at 8:00 AM per PRD requirements. Double shifts like
            "Tuesday-Wednesday" use the first day (Tuesday) as the start day.
        """
        # Handle double shifts like "Tuesday-Wednesday" -> use "Tuesday"
        day_name = shift.day_of_week.split('-')[0]

        # Get the day offset (Monday = 0, Tuesday = 1, etc.)
        day_offset = self.DAY_OFFSET_MAP[day_name]

        # Calculate the actual datetime: base Monday + week/day offsets
        # Then set to 8:00 AM using replace()
        shift_start = base_monday + timedelta(days=(week * 7) + day_offset)
        shift_start = shift_start.replace(hour=8, minute=0, second=0, microsecond=0)

        return shift_start
