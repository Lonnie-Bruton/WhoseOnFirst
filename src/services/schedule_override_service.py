"""
Schedule override service for business logic.

Handles manual shift overrides for vacation, sick days, and shift swaps.
Provides validation and snapshot creation for override operations.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from ..repositories.schedule_override_repository import ScheduleOverrideRepository
from ..repositories.schedule_repository import ScheduleRepository
from ..repositories.team_member_repository import TeamMemberRepository
from ..models.schedule_override import ScheduleOverride


class ScheduleOverrideService:
    """
    Service for managing schedule overrides.

    Provides business logic for creating, canceling, and querying
    manual schedule overrides without affecting rotation algorithm.

    Attributes:
        db: Database session
        override_repo: ScheduleOverride repository instance
        schedule_repo: Schedule repository instance
        team_member_repo: TeamMember repository instance
    """

    def __init__(self, db: Session):
        """
        Initialize ScheduleOverrideService.

        Args:
            db: Database session
        """
        self.db = db
        self.override_repo = ScheduleOverrideRepository(db)
        self.schedule_repo = ScheduleRepository(db)
        self.team_member_repo = TeamMemberRepository(db)

    def create_override(
        self,
        schedule_id: int,
        override_member_id: int,
        reason: Optional[str],
        created_by: str
    ) -> ScheduleOverride:
        """
        Create schedule override with validation.

        Validates that:
        1. Schedule exists
        2. Override member exists and is active
        3. No duplicate active override for same schedule
        4. Override member is different from original assignee

        Creates override with snapshot of member names for historical accuracy.

        Args:
            schedule_id: Schedule ID to override
            override_member_id: Team member ID covering the shift
            reason: Reason for override (vacation, sick, swap, etc.)
            created_by: Admin username creating the override

        Returns:
            ScheduleOverride: Created override instance

        Raises:
            ValueError: If validation fails
        """
        # Validation 1: Schedule exists
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule not found: {schedule_id}")

        # Validation 2: Override member exists
        override_member = self.team_member_repo.get_by_id(override_member_id)
        if not override_member:
            raise ValueError(f"Team member not found: {override_member_id}")

        # Validation 3: No duplicate active override
        existing = self.override_repo.get_override_for_schedule(schedule_id)
        if existing:
            raise ValueError(
                f"Active override already exists for this schedule (override ID: {existing.id})"
            )

        # Validation 4: Different from original
        if schedule.team_member_id == override_member_id:
            raise ValueError("Override member must be different from original assignee")

        # Create override with snapshots for historical accuracy
        override_data = {
            "schedule_id": schedule_id,
            "override_member_id": override_member_id,
            "original_member_name": schedule.team_member.name,
            "override_member_name": override_member.name,
            "reason": reason,
            "status": "active",
            "created_by": created_by,
        }

        return self.override_repo.create(override_data)

    def cancel_override(self, override_id: int) -> Optional[ScheduleOverride]:
        """
        Cancel an override (soft delete).

        Sets status to 'cancelled' and records cancellation timestamp.
        Does not physically delete the override from database.

        Args:
            override_id: ID of override to cancel

        Returns:
            Updated ScheduleOverride instance if found, None otherwise
        """
        return self.override_repo.cancel_override(override_id)

    def get_override_by_id(self, override_id: int) -> Optional[ScheduleOverride]:
        """
        Get override by ID.

        Args:
            override_id: Override ID

        Returns:
            ScheduleOverride instance if found, None otherwise
        """
        return self.override_repo.get_by_id(override_id)

    def get_override_display(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        """
        Get override display info for calendar rendering.

        Returns formatted override information for dashboard display,
        including override member, original member, reason, and icon.

        Args:
            schedule_id: Schedule ID to check for override

        Returns:
            Dictionary with override display info, or None if no active override
            Format: {
                "override_member": dict,
                "original_member_name": str,
                "reason": str,
                "icon": str,
                "created_by": str,
                "created_at": str (ISO format)
            }
        """
        override = self.override_repo.get_override_for_schedule(schedule_id)
        if not override:
            return None

        return {
            "override_member": override.override_member.to_dict(),
            "original_member_name": override.original_member_name,
            "reason": override.reason,
            "icon": "🔄",
            "created_by": override.created_by,
            "created_at": override.created_at.isoformat()
        }

    def get_all_active_overrides_map(self) -> Dict[int, ScheduleOverride]:
        """
        Get all active overrides as a map of schedule_id -> ScheduleOverride.

        Useful for dashboard calendar rendering to check overrides in bulk
        without making multiple database queries.

        Returns:
            Dictionary mapping schedule_id to ScheduleOverride instance
        """
        overrides = self.override_repo.get_active_overrides()
        return {o.schedule_id: o for o in overrides}

    def get_paginated_overrides(
        self,
        page: int = 1,
        per_page: int = 25,
        status: Optional[str] = None
    ) -> tuple[list[ScheduleOverride], Dict[str, Any]]:
        """
        Get paginated list of overrides with metadata.

        Args:
            page: Page number (1-indexed)
            per_page: Number of items per page
            status: Optional status filter (active, cancelled, completed)

        Returns:
            Tuple of (list of overrides, pagination metadata dict)
            Pagination dict format: {
                "page": int,
                "per_page": int,
                "total": int,
                "pages": int,
                "has_prev": bool,
                "has_next": bool
            }
        """
        overrides, total = self.override_repo.get_paginated(
            page=page,
            per_page=per_page,
            status=status,
            include_schedule=True
        )

        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1

        pagination = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages
        }

        return overrides, pagination
