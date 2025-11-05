"""
Team Members API Routes

FastAPI router for team member CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from src.api.dependencies import get_db
from src.api.schemas.team_member import (
    TeamMemberCreate,
    TeamMemberUpdate,
    TeamMemberResponse
)
from src.services import (
    TeamMemberService,
    DuplicatePhoneError,
    MemberNotFoundError,
    InvalidPhoneError
)


router = APIRouter()


@router.get("/", response_model=List[TeamMemberResponse])
def list_team_members(
    active_only: bool = Query(
        False,
        description="Filter to only active team members"
    ),
    db: Session = Depends(get_db)
):
    """
    List all team members.

    Args:
        active_only: If True, only return active members
        db: Database session (injected)

    Returns:
        List of team members

    Example:
        GET /api/v1/team-members/?active_only=true
    """
    service = TeamMemberService(db)
    if active_only:
        members = service.get_active()
    else:
        members = service.get_all()
    return members


@router.get("/{member_id}", response_model=TeamMemberResponse)
def get_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific team member by ID.

    Args:
        member_id: Team member ID
        db: Database session (injected)

    Returns:
        Team member details

    Raises:
        HTTPException: 404 if member not found

    Example:
        GET /api/v1/team-members/1
    """
    service = TeamMemberService(db)
    try:
        member = service.get_by_id(member_id)
        return member
    except MemberNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
def create_team_member(
    member_data: TeamMemberCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new team member.

    Args:
        member_data: Team member creation data
        db: Database session (injected)

    Returns:
        Created team member

    Raises:
        HTTPException: 400 if phone already exists or phone format invalid

    Example:
        POST /api/v1/team-members/
        {
            "name": "John Doe",
            "phone": "+15551234567"
        }
    """
    service = TeamMemberService(db)
    try:
        member = service.create(member_data.model_dump())
        return member
    except DuplicatePhoneError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidPhoneError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{member_id}", response_model=TeamMemberResponse)
def update_team_member(
    member_id: int,
    member_data: TeamMemberUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing team member.

    Args:
        member_id: Team member ID
        member_data: Team member update data
        db: Database session (injected)

    Returns:
        Updated team member

    Raises:
        HTTPException: 404 if member not found, 400 if phone already exists

    Example:
        PUT /api/v1/team-members/1
        {
            "name": "John Smith"
        }
    """
    service = TeamMemberService(db)
    try:
        member = service.update(member_id, member_data.model_dump(exclude_unset=True))
        return member
    except MemberNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicatePhoneError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidPhoneError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Deactivate a team member (soft delete).

    This removes them from rotation but preserves their schedule history.

    Args:
        member_id: Team member ID
        db: Database session (injected)

    Returns:
        No content

    Raises:
        HTTPException: 404 if member not found

    Example:
        DELETE /api/v1/team-members/1
    """
    service = TeamMemberService(db)
    try:
        service.deactivate(member_id)
        return None
    except MemberNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{member_id}/activate", response_model=TeamMemberResponse)
def activate_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Reactivate a deactivated team member.

    This adds them back to the rotation.

    Args:
        member_id: Team member ID
        db: Database session (injected)

    Returns:
        Activated team member

    Raises:
        HTTPException: 404 if member not found

    Example:
        POST /api/v1/team-members/1/activate
    """
    service = TeamMemberService(db)
    try:
        member = service.activate(member_id)
        return member
    except MemberNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
