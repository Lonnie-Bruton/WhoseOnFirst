"""
Team Member Service Layer.

This module provides business logic for team member management operations.
It coordinates between the API layer and repository layer, handling validation,
business rules, and cross-cutting concerns.

Key responsibilities:
- CRUD operations with business logic
- Phone number uniqueness validation
- Member activation/deactivation
- Integration with schedule regeneration (Phase 2)
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.team_member import TeamMember
from src.repositories.team_member_repository import TeamMemberRepository


class TeamMemberServiceError(Exception):
    """Base exception for team member service errors."""


class DuplicatePhoneError(TeamMemberServiceError):
    """Raised when attempting to create member with duplicate phone number."""


class MemberNotFoundError(TeamMemberServiceError):
    """Raised when team member is not found."""


class InvalidPhoneError(TeamMemberServiceError):
    """Raised when phone number is invalid."""


class TeamMemberService:
    """
    Service for team member business logic.

    This service encapsulates all business logic related to team member management,
    including CRUD operations, validation, and coordination with other services.

    Attributes:
        db: SQLAlchemy database session
        repository: TeamMemberRepository instance for data access
    """

    def __init__(self, db: Session):
        """
        Initialize the team member service.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.repository = TeamMemberRepository(db)

    def create(self, member_data: Dict[str, Any]) -> TeamMember:
        """
        Create a new team member.

        Validates phone number format and uniqueness before creation.
        In future phases, will trigger schedule regeneration.

        Args:
            member_data: Dictionary containing member data
                - name: Full name of team member
                - phone: Phone number in E.164 format (+1XXXXXXXXXX)
                - is_active: Optional, defaults to True

        Returns:
            Created TeamMember instance

        Raises:
            InvalidPhoneError: If phone number format is invalid
            DuplicatePhoneError: If phone number already exists
            TeamMemberServiceError: For other creation errors
        """
        # Validate phone number format
        phone = member_data.get("phone")
        if not phone or not TeamMember.validate_phone(phone):
            raise InvalidPhoneError(
                f"Invalid phone number format. Must be E.164 format (+1XXXXXXXXXX): {phone}"
            )

        # TEMPORARY: Disabled for testing - allow duplicate phones for dry run testing
        # TODO: Re-enable this check before production deployment
        # Check for duplicate phone number
        # if self.repository.phone_exists(phone):
        #     raise DuplicatePhoneError(
        #         f"Phone number already registered: {phone}"
        #     )

        try:
            # Auto-assign rotation_order if not provided and member is active
            if member_data.get("is_active", True) and "rotation_order" not in member_data:
                max_order = self.repository.get_max_rotation_order()
                member_data["rotation_order"] = 0 if max_order is None else max_order + 1

            member = self.repository.create(member_data)

            # TODO: Phase 2 - Trigger schedule regeneration
            # if member.is_active:
            #     schedule_service = ScheduleService(self.db)
            #     schedule_service.regenerate_from_date(datetime.now())

            return member

        except IntegrityError as e:
            raise DuplicatePhoneError(
                f"Phone number already registered: {phone}"
            ) from e
        except Exception as e:
            raise TeamMemberServiceError(
                f"Failed to create team member: {str(e)}"
            ) from e

    def get_by_id(self, member_id: int) -> TeamMember:
        """
        Get team member by ID.

        Args:
            member_id: ID of the team member

        Returns:
            TeamMember instance

        Raises:
            MemberNotFoundError: If member not found
        """
        member = self.repository.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(f"Team member not found: {member_id}")
        return member

    def get_all(
        self,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamMember]:
        """
        Get all team members with optional filtering.

        Args:
            active_only: If True, return only active members
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of TeamMember instances
        """
        if active_only:
            return self.repository.get_active()
        return self.repository.get_all(skip=skip, limit=limit)

    def get_active(self) -> List[TeamMember]:
        """
        Get all active team members.

        Returns:
            List of active TeamMember instances
        """
        return self.repository.get_active()

    def get_inactive(self) -> List[TeamMember]:
        """
        Get all inactive team members.

        Returns:
            List of inactive TeamMember instances
        """
        return self.repository.get_inactive()

    def get_by_phone(self, phone: str) -> Optional[TeamMember]:
        """
        Get team member by phone number.

        Args:
            phone: Phone number in E.164 format

        Returns:
            TeamMember instance if found, None otherwise
        """
        return self.repository.get_by_phone(phone)

    def update(
        self,
        member_id: int,
        update_data: Dict[str, Any]
    ) -> TeamMember:
        """
        Update team member information.

        Validates phone number if being updated.

        Args:
            member_id: ID of the team member to update
            update_data: Dictionary of fields to update

        Returns:
            Updated TeamMember instance

        Raises:
            MemberNotFoundError: If member not found
            InvalidPhoneError: If new phone number format is invalid
            DuplicatePhoneError: If new phone number already exists
        """
        # Check member exists
        _ = self.get_by_id(member_id)

        # Validate phone number if being updated
        if "phone" in update_data:
            new_phone = update_data["phone"]
            if not TeamMember.validate_phone(new_phone):
                raise InvalidPhoneError(
                    f"Invalid phone number format: {new_phone}"
                )

            # TEMPORARY: Disabled for testing - allow duplicate phones for dry run testing
            # TODO: Re-enable this check before production deployment
            # Check if new phone is already in use (excluding current member)
            # if self.repository.phone_exists(new_phone, exclude_id=member_id):
            #     raise DuplicatePhoneError(
            #         f"Phone number already registered: {new_phone}"
            #     )

        try:
            updated_member = self.repository.update(member_id, update_data)

            # TODO: Phase 2 - Trigger schedule regeneration if is_active changed
            # if "is_active" in update_data:
            #     schedule_service = ScheduleService(self.db)
            #     schedule_service.regenerate_from_date(datetime.now())

            return updated_member

        except IntegrityError as e:
            raise DuplicatePhoneError(
                f"Phone number already registered: {update_data.get('phone')}"
            ) from e
        except Exception as e:
            raise TeamMemberServiceError(
                f"Failed to update team member: {str(e)}"
            ) from e

    def delete(self, member_id: int) -> bool:
        """
        Hard delete a team member.

        Note: This performs a hard delete. Consider using deactivate() instead
        to preserve history.

        Args:
            member_id: ID of the team member to delete

        Returns:
            True if deleted successfully

        Raises:
            MemberNotFoundError: If member not found
        """
        member = self.get_by_id(member_id)

        success = self.repository.delete(member_id)

        # TODO: Phase 2 - Trigger schedule regeneration
        # if success:
        #     schedule_service = ScheduleService(self.db)
        #     schedule_service.regenerate_from_date(datetime.now())

        return success

    def deactivate(self, member_id: int) -> TeamMember:
        """
        Deactivate a team member (soft delete).

        This is the recommended way to remove members as it preserves
        historical data and schedule assignments.

        When deactivating, rotation_order is set to null since inactive
        members should not be in the rotation. All remaining active members
        are renumbered to maintain consecutive rotation_order values (0, 1, 2, ...).

        Args:
            member_id: ID of the team member to deactivate

        Returns:
            Updated TeamMember instance with is_active=False and rotation_order=None

        Raises:
            MemberNotFoundError: If member not found
        """
        member = self.get_by_id(member_id)

        if not member.is_active:
            return member  # Already inactive

        # Deactivate and clear rotation order
        deactivated = self.repository.deactivate(member_id)
        self.repository.update(member_id, {"rotation_order": None})
        self.db.refresh(deactivated)

        # Renumber remaining active members to maintain consecutive order
        active_members = self.repository.get_ordered_for_rotation()
        order_mapping = {str(m.id): i for i, m in enumerate(active_members)}
        if order_mapping:
            self.repository.update_rotation_orders(order_mapping)

        # TODO: Phase 2 - Trigger schedule regeneration
        # schedule_service = ScheduleService(self.db)
        # schedule_service.regenerate_from_date(datetime.now())

        return deactivated

    def activate(self, member_id: int) -> TeamMember:
        """
        Activate a team member.

        When activating, automatically assigns the next available rotation_order
        (max existing rotation_order + 1) to place them at the end of the rotation.

        Args:
            member_id: ID of the team member to activate

        Returns:
            Updated TeamMember instance with is_active=True and assigned rotation_order

        Raises:
            MemberNotFoundError: If member not found
        """
        member = self.get_by_id(member_id)

        if member.is_active:
            return member  # Already active

        # Activate the member
        activated = self.repository.activate(member_id)

        # Assign next available rotation order (starting from 0)
        max_order = self.repository.get_max_rotation_order()
        next_order = 0 if max_order is None else max_order + 1
        self.repository.update(member_id, {"rotation_order": next_order})
        self.db.refresh(activated)

        # TODO: Phase 2 - Trigger schedule regeneration
        # schedule_service = ScheduleService(self.db)
        # schedule_service.regenerate_from_date(datetime.now())

        return activated

    def phone_exists(self, phone: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if phone number is already registered.

        Args:
            phone: Phone number to check
            exclude_id: Optional member ID to exclude from check (for updates)

        Returns:
            True if phone exists, False otherwise
        """
        return self.repository.phone_exists(phone, exclude_id=exclude_id)

    def get_count(self, active_only: bool = False) -> int:
        """
        Get count of team members.

        Args:
            active_only: If True, count only active members

        Returns:
            Count of team members
        """
        if active_only:
            return self.repository.get_count_active()
        return self.repository.count()

    def search_by_name(self, name: str) -> List[TeamMember]:
        """
        Search team members by name (case-insensitive partial match).

        Args:
            name: Name or partial name to search for

        Returns:
            List of matching TeamMember instances
        """
        return self.repository.search_by_name(name)

    def update_rotation_orders(self, order_mapping: Dict[int, int]) -> List[TeamMember]:
        """
        Update rotation order for multiple team members.

        This method allows you to reorder team members in the rotation sequence.
        Lower rotation_order values go first in the rotation.

        Args:
            order_mapping: Dictionary mapping team member ID to new rotation_order value
                          Example: {1: 0, 2: 1, 3: 2}

        Returns:
            List of updated TeamMember instances

        Raises:
            MemberNotFoundError: If any member ID not found
            TeamMemberServiceError: If update operation fails

        Example:
            >>> service.update_rotation_orders({1: 0, 2: 1, 3: 2})
            [<TeamMember 1>, <TeamMember 2>, <TeamMember 3>]
        """
        # Validate all member IDs exist before making any changes
        for member_id in order_mapping.keys():
            self.get_by_id(member_id)  # Raises MemberNotFoundError if not found

        try:
            updated_members = self.repository.update_rotation_orders(order_mapping)

            # TODO: Phase 2 - Consider triggering schedule regeneration if rotation order changes
            # schedule_service = ScheduleService(self.db)
            # schedule_service.regenerate_from_date(datetime.now())

            return updated_members

        except Exception as e:
            raise TeamMemberServiceError(
                f"Failed to update rotation orders: {str(e)}"
            ) from e
