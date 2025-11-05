"""
Team Member Pydantic Schemas

Request and response models for team member API endpoints.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class TeamMemberBase(BaseModel):
    """
    Base schema for team member with common fields.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Team member's full name",
        examples=["John Doe"]
    )
    phone: str = Field(
        ...,
        pattern=r'^\+1\d{10}$',
        description="Phone number in E.164 format (+1XXXXXXXXXX)",
        examples=["+15551234567"]
    )

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v: str) -> str:
        """
        Validate phone number is in E.164 format.

        Args:
            v: Phone number string

        Returns:
            str: Validated phone number

        Raises:
            ValueError: If phone format is invalid
        """
        if not re.match(r'^\+1\d{10}$', v):
            raise ValueError(
                'Phone must be in E.164 format (+1XXXXXXXXXX). '
                'Example: +15551234567'
            )
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validate and clean team member name.

        Args:
            v: Name string

        Returns:
            str: Cleaned name

        Raises:
            ValueError: If name is empty or whitespace only
        """
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty or whitespace only')
        return v


class TeamMemberCreate(TeamMemberBase):
    """
    Schema for creating a new team member.

    All fields from TeamMemberBase are required.
    """
    pass


class TeamMemberUpdate(BaseModel):
    """
    Schema for updating an existing team member.

    All fields are optional to support partial updates.
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Team member's full name",
        examples=["John Doe"]
    )
    phone: Optional[str] = Field(
        None,
        pattern=r'^\+1\d{10}$',
        description="Phone number in E.164 format (+1XXXXXXXXXX)",
        examples=["+15551234567"]
    )

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate phone number is in E.164 format if provided.

        Args:
            v: Phone number string or None

        Returns:
            Optional[str]: Validated phone number or None

        Raises:
            ValueError: If phone format is invalid
        """
        if v is not None and not re.match(r'^\+1\d{10}$', v):
            raise ValueError(
                'Phone must be in E.164 format (+1XXXXXXXXXX). '
                'Example: +15551234567'
            )
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate and clean team member name if provided.

        Args:
            v: Name string or None

        Returns:
            Optional[str]: Cleaned name or None

        Raises:
            ValueError: If name is empty or whitespace only
        """
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Name cannot be empty or whitespace only')
        return v


class TeamMemberResponse(TeamMemberBase):
    """
    Schema for team member responses.

    Includes all fields from TeamMemberBase plus database fields.
    """
    id: int = Field(
        ...,
        description="Unique team member ID",
        examples=[1]
    )
    is_active: bool = Field(
        ...,
        description="Whether the team member is active",
        examples=[True]
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the team member was created",
        examples=["2025-01-01T00:00:00"]
    )

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "phone": "+15551234567",
                "is_active": True,
                "created_at": "2025-01-01T00:00:00"
            }
        }
