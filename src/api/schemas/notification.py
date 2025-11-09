"""
Notification API Schemas

Pydantic models for notification log requests and responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NotificationLogResponse(BaseModel):
    """Response schema for notification log entries."""

    id: int = Field(..., description="Notification log ID")
    schedule_id: int = Field(..., description="Associated schedule ID")
    sent_at: datetime = Field(..., description="Timestamp when notification was sent")
    status: str = Field(..., description="Notification status (sent, failed, delivered, etc.)")
    twilio_sid: Optional[str] = Field(None, description="Twilio message SID")
    error_message: Optional[str] = Field(None, description="Error details if failed")

    class Config:
        from_attributes = True


class NotificationStatsResponse(BaseModel):
    """Response schema for notification statistics."""

    total_sent: int = Field(..., description="Total notifications sent in period")
    this_month: int = Field(..., description="Notifications sent this month")
    delivery_rate: float = Field(..., description="Success rate percentage (0-100)")
    failed_count: int = Field(..., description="Number of failed notifications")
    sent_count: int = Field(..., description="Number of sent (not yet delivered)")
    delivered_count: int = Field(..., description="Number of confirmed delivered")
    pending_count: int = Field(..., description="Number still pending")
    period_days: int = Field(..., description="Number of days in the stats period")

    class Config:
        from_attributes = True
