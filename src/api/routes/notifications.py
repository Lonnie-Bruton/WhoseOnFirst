"""
Notifications API Routes

FastAPI router for SMS notification management and history.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from src.api.dependencies import get_db
from src.api.schemas.notification import (
    NotificationLogResponse,
    NotificationStatsResponse
)
from src.repositories.notification_log_repository import NotificationLogRepository
from src.api.routes.auth import require_auth


router = APIRouter()


@router.get("/recent", response_model=List[NotificationLogResponse])
def get_recent_notifications(
    limit: int = Query(
        50,
        ge=1,
        le=100,
        description="Number of recent notifications to retrieve (1-100)"
    ),
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get recent notification logs.

    Returns the most recent SMS notification attempts, ordered by timestamp descending.

    Args:
        limit: Maximum number of notifications to return (default 50)
        db: Database session (injected)

    Returns:
        List of recent notification log entries with schedule and member details

    Example:
        GET /api/v1/notifications/recent?limit=10
    """
    repo = NotificationLogRepository(db)
    logs = repo.get_recent_logs(limit=limit, include_schedule=True)
    return logs


@router.get("/stats", response_model=NotificationStatsResponse)
def get_notification_stats(
    days: int = Query(
        30,
        ge=1,
        le=365,
        description="Number of days to calculate stats for (1-365)"
    ),
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get notification statistics and success metrics.

    Calculates delivery rates, total counts, and status breakdowns
    for the specified time period.

    Args:
        days: Number of days to include in calculation (default 30)
        db: Database session (injected)

    Returns:
        Statistics summary including counts, rates, and trends

    Example:
        GET /api/v1/notifications/stats?days=30
    """
    repo = NotificationLogRepository(db)

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Get success rate metrics
    stats = repo.get_success_rate(start_date=start_date, end_date=end_date)

    # Get this month's count
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = repo.get_by_date_range(month_start, end_date, include_schedule=False)

    return {
        "total_sent": stats["total"],
        "this_month": len(this_month),
        "delivery_rate": stats["success_rate"],
        "failed_count": stats["failed"] + stats["undelivered"],
        "sent_count": stats["sent"],
        "delivered_count": stats["delivered"],
        "pending_count": stats["pending"],
        "period_days": days
    }


@router.get("/failed", response_model=List[NotificationLogResponse])
def get_failed_notifications(
    hours: int = Query(
        24,
        ge=1,
        le=168,
        description="Number of hours to look back (1-168)"
    ),
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get failed notification attempts.

    Returns recent failed or undelivered notifications for troubleshooting.

    Args:
        hours: Number of hours to look back (default 24)
        db: Database session (injected)

    Returns:
        List of failed notification log entries

    Example:
        GET /api/v1/notifications/failed?hours=48
    """
    repo = NotificationLogRepository(db)
    failed = repo.get_failed_notifications(hours_ago=hours)
    return failed


@router.get("/{notification_id}", response_model=NotificationLogResponse)
def get_notification_by_id(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get a specific notification log by ID.

    Args:
        notification_id: Notification log ID
        db: Database session (injected)

    Returns:
        Notification log entry with schedule details

    Example:
        GET /api/v1/notifications/1
    """
    repo = NotificationLogRepository(db)
    log = repo.get_by_id(notification_id)

    if not log:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification log not found: {notification_id}"
        )

    return log
