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
