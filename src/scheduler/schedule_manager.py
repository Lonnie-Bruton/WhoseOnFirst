"""
Schedule Manager - APScheduler Integration

This module manages the background scheduler for automated daily notifications.
It configures APScheduler to send SMS notifications at 8:00 AM CST daily.

Key responsibilities:
- Initialize and configure BackgroundScheduler
- Schedule daily notification job at 8:00 AM America/Chicago
- Provide lifecycle management (start, stop, shutdown)
- Query pending notifications and trigger SMS delivery
"""

import logging
from datetime import datetime
from typing import Optional, List
from contextlib import contextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from pytz import timezone
from sqlalchemy.orm import Session

from src.models.database import SessionLocal
from src.services.schedule_service import ScheduleService
from src.services.sms_service import SMSService
from src.models.schedule import Schedule


# Configure logging
logger = logging.getLogger(__name__)


# Chicago timezone for scheduler
CHICAGO_TZ = timezone('America/Chicago')


class ScheduleManager:
    """
    Manager for scheduling automated notifications.

    This class wraps APScheduler's BackgroundScheduler and provides
    methods to start, stop, and manage the daily notification job.

    Attributes:
        scheduler: APScheduler BackgroundScheduler instance
        is_running: Whether the scheduler is currently running
    """

    def __init__(self):
        """
        Initialize the schedule manager.

        Creates a BackgroundScheduler configured with:
        - America/Chicago timezone
        - Memory job store (can be upgraded to SQLAlchemy store later)
        - Coalesce for missed jobs
        """
        self.scheduler = BackgroundScheduler(
            jobstores={'default': MemoryJobStore()},
            timezone=CHICAGO_TZ,
            job_defaults={
                'coalesce': True,  # Combine multiple missed runs into one
                'max_instances': 1,  # Only one instance of job can run at a time
                'misfire_grace_time': 300  # 5 minute grace period for missed jobs
            }
        )
        self.is_running = False
        logger.info("ScheduleManager initialized with timezone: %s", CHICAGO_TZ)

    def add_daily_notification_job(self) -> None:
        """
        Add the daily notification job to the scheduler.

        Configures a CronTrigger to run send_daily_notifications()
        every day at 8:00 AM Chicago time.

        The job will:
        - Query schedules that start today and haven't been notified
        - Send SMS notifications via Twilio
        - Mark schedules as notified
        """
        self.scheduler.add_job(
            func=send_daily_notifications,
            trigger=CronTrigger(hour=8, minute=0, timezone=CHICAGO_TZ),
            id='daily_oncall_notifications',
            name='Daily On-Call SMS Notifications',
            replace_existing=True
        )
        logger.info("Added daily notification job: 8:00 AM %s", CHICAGO_TZ)

    def start(self) -> None:
        """
        Start the scheduler.

        This should be called during application startup (e.g., in FastAPI lifespan).

        Raises:
            RuntimeError: If scheduler is already running
        """
        if self.is_running:
            logger.warning("Scheduler is already running")
            return

        self.add_daily_notification_job()
        self.scheduler.start()
        self.is_running = True
        logger.info("Scheduler started successfully")

        # Log scheduled jobs
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            logger.info("Scheduled job: %s (next run: %s)", job.name, job.next_run_time)

    def stop(self, wait: bool = True) -> None:
        """
        Stop the scheduler.

        This should be called during application shutdown.

        Args:
            wait: If True, wait for currently executing jobs to finish
        """
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return

        self.scheduler.shutdown(wait=wait)
        self.is_running = False
        logger.info("Scheduler stopped")

    def trigger_job_now(self, job_id: str = 'daily_oncall_notifications') -> None:
        """
        Manually trigger a scheduled job immediately.

        Useful for testing and manual execution.

        Args:
            job_id: ID of the job to trigger

        Raises:
            LookupError: If job with given ID doesn't exist
        """
        job = self.scheduler.get_job(job_id)
        if not job:
            raise LookupError(f"Job with ID '{job_id}' not found")

        logger.info("Manually triggering job: %s", job_id)
        job.modify(next_run_time=datetime.now(CHICAGO_TZ))

    def get_job_status(self, job_id: str = 'daily_oncall_notifications') -> Optional[dict]:
        """
        Get the status of a scheduled job.

        Args:
            job_id: ID of the job to check

        Returns:
            Dictionary with job information, or None if job not found
        """
        job = self.scheduler.get_job(job_id)
        if not job:
            return None

        return {
            'id': job.id,
            'name': job.name,
            'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
            'trigger': str(job.trigger)
        }


# Singleton instance
_schedule_manager: Optional[ScheduleManager] = None


def get_schedule_manager() -> ScheduleManager:
    """
    Get the global ScheduleManager instance (singleton pattern).

    Returns:
        ScheduleManager: The global scheduler instance
    """
    global _schedule_manager
    if _schedule_manager is None:
        _schedule_manager = ScheduleManager()
    return _schedule_manager


@contextmanager
def get_db_session():
    """
    Context manager for database sessions in scheduled jobs.

    Ensures proper session cleanup even if job fails.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def send_daily_notifications() -> None:
    """
    Send daily on-call notifications via SMS.

    This function is executed by APScheduler every day at 8:00 AM CST.

    Process:
    1. Get today's date in America/Chicago timezone
    2. Query schedules that start today and haven't been notified
    3. For each schedule, send SMS notification via Twilio
    4. Mark schedule as notified in database
    5. Log results

    Note: This function runs in a background thread, so it must manage
    its own database session.
    """
    logger.info("Starting daily notification job")

    # Get current date in Chicago timezone
    now = datetime.now(CHICAGO_TZ)
    today = now.date()

    logger.info("Processing notifications for date: %s", today)

    # Use context manager for database session
    with get_db_session() as db:
        try:
            # Get schedules that need notifications
            service = ScheduleService(db)
            pending_schedules = service.get_pending_notifications(target_date=now)

            if not pending_schedules:
                logger.info("No pending notifications for today")
                return

            logger.info("Found %d schedules requiring notification", len(pending_schedules))

            # Initialize SMS service
            sms_service = SMSService(db)

            # Send notifications using batch method
            result = sms_service.send_batch_notifications(pending_schedules, force=False)

            logger.info(
                "Notification job complete: %d successful, %d failed, %d skipped out of %d total",
                result['successful'],
                result['failed'],
                result['skipped'],
                result['total']
            )

        except Exception as e:
            logger.error("Error in daily notification job: %s", str(e), exc_info=True)
            raise


def trigger_notifications_manually() -> dict:
    """
    Manually trigger the notification job for testing.

    This function can be called from an API endpoint to test
    the notification system without waiting for the scheduled time.

    Returns:
        dict: Result summary with counts and status
    """
    logger.info("Manual notification trigger requested")

    try:
        send_daily_notifications()
        return {
            'status': 'success',
            'message': 'Notifications processed successfully',
            'timestamp': datetime.now(CHICAGO_TZ).isoformat()
        }
    except Exception as e:
        logger.error("Manual notification trigger failed: %s", str(e))
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now(CHICAGO_TZ).isoformat()
        }
