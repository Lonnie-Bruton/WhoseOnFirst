"""
Shifts API Routes

FastAPI router for shift configuration CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.api.dependencies import get_db
from src.api.schemas.shift import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse
)
from src.services import (
    ShiftService,
    DuplicateShiftNumberError,
    ShiftNotFoundError,
    InvalidShiftDataError
)


router = APIRouter()


@router.get("/", response_model=List[ShiftResponse])
def list_shifts(
    db: Session = Depends(get_db)
):
    """
    List all shift configurations.

    Args:
        db: Database session (injected)

    Returns:
        List of shift configurations ordered by shift_number

    Example:
        GET /api/v1/shifts/
    """
    service = ShiftService(db)
    shifts = service.get_all()
    return shifts


@router.get("/{shift_id}", response_model=ShiftResponse)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific shift configuration by ID.

    Args:
        shift_id: Shift configuration ID
        db: Database session (injected)

    Returns:
        Shift configuration details

    Raises:
        HTTPException: 404 if shift not found

    Example:
        GET /api/v1/shifts/1
    """
    service = ShiftService(db)
    try:
        shift = service.get_by_id(shift_id)
        return shift
    except ShiftNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=ShiftResponse, status_code=status.HTTP_201_CREATED)
def create_shift(
    shift_data: ShiftCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new shift configuration.

    Args:
        shift_data: Shift creation data
        db: Database session (injected)

    Returns:
        Created shift configuration

    Raises:
        HTTPException: 400 if shift number already exists or validation fails

    Example:
        POST /api/v1/shifts/
        {
            "shift_number": 1,
            "day_of_week": "Monday",
            "duration_hours": 24,
            "start_time": "08:00"
        }
    """
    service = ShiftService(db)
    try:
        shift = service.create(shift_data.model_dump())
        return shift
    except DuplicateShiftNumberError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidShiftDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{shift_id}", response_model=ShiftResponse)
def update_shift(
    shift_id: int,
    shift_data: ShiftUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing shift configuration.

    Args:
        shift_id: Shift configuration ID
        shift_data: Shift update data
        db: Database session (injected)

    Returns:
        Updated shift configuration

    Raises:
        HTTPException: 404 if shift not found, 400 if validation fails

    Example:
        PUT /api/v1/shifts/1
        {
            "day_of_week": "Tuesday",
            "duration_hours": 48
        }
    """
    service = ShiftService(db)
    try:
        shift = service.update(shift_id, shift_data.model_dump(exclude_unset=True))
        return shift
    except ShiftNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (DuplicateShiftNumberError, InvalidShiftDataError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a shift configuration.

    WARNING: This will cascade delete all schedule assignments for this shift.
    Use with caution in production.

    Args:
        shift_id: Shift configuration ID
        db: Database session (injected)

    Returns:
        No content

    Raises:
        HTTPException: 404 if shift not found

    Example:
        DELETE /api/v1/shifts/1
    """
    service = ShiftService(db)
    try:
        service.delete(shift_id)
        return None
    except ShiftNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
