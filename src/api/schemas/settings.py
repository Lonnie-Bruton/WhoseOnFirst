"""
Pydantic schemas for settings API.

Defines request/response models for settings endpoints.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime


class SettingResponse(BaseModel):
    """Response model for a single setting."""

    id: int
    key: str
    value: str
    value_type: str
    description: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class SettingUpdateRequest(BaseModel):
    """Request model for updating a setting."""

    value: Any = Field(..., description="Setting value (will be converted to appropriate type)")


class AutoRenewConfigResponse(BaseModel):
    """Response model for auto-renewal configuration."""

    enabled: bool = Field(..., description="Whether auto-renewal is enabled")
    threshold_weeks: int = Field(..., description="Weeks remaining to trigger renewal", ge=1, le=52)
    renew_weeks: int = Field(..., description="Number of weeks to generate during renewal", ge=1, le=104)


class AutoRenewConfigRequest(BaseModel):
    """Request model for updating auto-renewal configuration."""

    enabled: Optional[bool] = Field(None, description="Enable or disable auto-renewal")
    threshold_weeks: Optional[int] = Field(None, description="Weeks remaining to trigger renewal", ge=1, le=52)
    renew_weeks: Optional[int] = Field(None, description="Number of weeks to generate", ge=1, le=104)


class SMSTemplateResponse(BaseModel):
    """Response model for SMS template."""

    template: str = Field(..., description="SMS notification template with variables")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    character_count: int = Field(..., description="Template character count")
    sms_count: int = Field(..., description="Estimated SMS segments (160 chars per SMS)")
    variables: list[str] = Field(..., description="List of template variables found")


class SMSTemplateRequest(BaseModel):
    """Request model for updating SMS template."""

    template: str = Field(
        ...,
        description="SMS template with variables: {name}, {start_time}, {end_time}, {duration}",
        min_length=1,
        max_length=320,
        examples=["WhoseOnFirst Alert\n\nHi {name}, you are on-call from {start_time} to {end_time}."]
    )


class EscalationConfigResponse(BaseModel):
    """Response model for escalation contact configuration."""

    enabled: bool = Field(..., description="Whether escalation contacts are displayed on dashboard")
    primary_name: Optional[str] = Field(None, description="Primary escalation contact name")
    primary_phone: Optional[str] = Field(None, description="Primary escalation contact phone (E.164 format)")
    secondary_name: Optional[str] = Field(None, description="Secondary escalation contact name")
    secondary_phone: Optional[str] = Field(None, description="Secondary escalation contact phone (E.164 format)")


class EscalationConfigRequest(BaseModel):
    """Request model for updating escalation contact configuration."""

    enabled: bool = Field(..., description="Enable or disable escalation contact display")
    primary_name: Optional[str] = Field(None, description="Primary escalation contact name", max_length=100)
    primary_phone: Optional[str] = Field(
        None,
        description="Primary escalation contact phone (E.164 format: +1XXXXXXXXXX)",
        pattern=r"^\+1\d{10}$",
        examples=["+19187019714"]
    )
    secondary_name: Optional[str] = Field(None, description="Secondary escalation contact name", max_length=100)
    secondary_phone: Optional[str] = Field(
        None,
        description="Secondary escalation contact phone (E.164 format: +1XXXXXXXXXX)",
        pattern=r"^\+1\d{10}$",
        examples=["+19187019714"]
    )
