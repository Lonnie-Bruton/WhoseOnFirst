"""
SMS service for sending notifications via Twilio.

Handles SMS delivery with retry logic, error handling, and notification logging.
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from time import sleep

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from sqlalchemy.orm import Session

from ..repositories import NotificationLogRepository, ScheduleRepository
from ..models import Schedule


logger = logging.getLogger(__name__)


class SMSServiceError(Exception):
    """Base exception for SMS service errors."""


class TwilioConfigurationError(SMSServiceError):
    """Raised when Twilio configuration is invalid or missing."""


class SMSDeliveryError(SMSServiceError):
    """Raised when SMS delivery fails after all retry attempts."""


class SMSService:
    """
    Service for sending SMS notifications via Twilio.

    Implements:
    - SMS message composition and delivery
    - Exponential backoff retry logic
    - Notification logging for audit trail
    - Error handling and recovery
    - Phone number formatting and validation

    Attributes:
        db: Database session
        twilio_client: Twilio REST client
        from_phone: Twilio phone number for sending messages
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
        notification_repo: Repository for logging notifications
        schedule_repo: Repository for schedule operations
    """

    def __init__(
        self,
        db: Session,
        max_retries: int = 3,
        base_delay: int = 60,
        mock_mode: bool = False
    ):
        """
        Initialize SMS service.

        Args:
            db: SQLAlchemy database session
            max_retries: Maximum retry attempts (default: 3)
            base_delay: Base delay in seconds for exponential backoff (default: 60)
            mock_mode: If True, skip Twilio client initialization for testing

        Raises:
            TwilioConfigurationError: If Twilio credentials are missing
        """
        self.db = db
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.mock_mode = mock_mode

        # Initialize repositories
        self.notification_repo = NotificationLogRepository(db)
        self.schedule_repo = ScheduleRepository(db)

        # Initialize Twilio client
        if not mock_mode:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            self.from_phone = os.getenv('TWILIO_PHONE_NUMBER')

            if not all([account_sid, auth_token, self.from_phone]):
                raise TwilioConfigurationError(
                    "Twilio configuration missing. Please set TWILIO_ACCOUNT_SID, "
                    "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER environment variables."
                )

            try:
                self.twilio_client = Client(account_sid, auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                raise TwilioConfigurationError(f"Failed to initialize Twilio client: {str(e)}")
        else:
            self.twilio_client = None
            self.from_phone = "+15551234567"  # Mock phone number
            logger.info("SMS service initialized in mock mode")

    def send_notification(
        self,
        schedule: Schedule,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Send SMS notification for a schedule assignment.

        Implements retry logic with exponential backoff:
        - Attempt 1: Immediate
        - Attempt 2: After 60 seconds (base_delay)
        - Attempt 3: After 120 seconds (base_delay * 2)
        - etc.

        Args:
            schedule: Schedule instance to send notification for
            force: If True, send even if already notified (default: False)

        Returns:
            Dictionary with result information:
            {
                "success": bool,
                "schedule_id": int,
                "twilio_sid": str or None,
                "status": str,
                "message": str,
                "attempts": int,
                "error": str or None
            }

        Raises:
            SMSServiceError: If schedule data is invalid
        """
        # Validate schedule
        if not schedule.team_member:
            raise SMSServiceError(f"Schedule {schedule.id} has no team member assigned")

        if not schedule.shift:
            raise SMSServiceError(f"Schedule {schedule.id} has no shift assigned")

        # Check if already notified
        if schedule.notified and not force:
            logger.info(f"Schedule {schedule.id} already notified, skipping")
            return {
                "success": True,
                "schedule_id": schedule.id,
                "twilio_sid": None,
                "status": "skipped",
                "message": "Already notified",
                "attempts": 0,
                "error": None
            }

        # Check retry count
        retry_count = self.notification_repo.get_retry_count_for_schedule(schedule.id)
        if retry_count >= self.max_retries:
            logger.warning(
                f"Schedule {schedule.id} exceeded max retries ({self.max_retries}), "
                "marking as failed"
            )
            self.notification_repo.log_notification_attempt(
                schedule_id=schedule.id,
                status='failed',
                error_message=f"Exceeded maximum retry attempts ({self.max_retries})",
                recipient_name=schedule.team_member.name,
                recipient_phone=schedule.team_member.phone
            )
            return {
                "success": False,
                "schedule_id": schedule.id,
                "twilio_sid": None,
                "status": "failed",
                "message": "Exceeded maximum retry attempts",
                "attempts": retry_count,
                "error": "Max retries exceeded"
            }

        # Compose message
        message_body = self._compose_message(schedule)
        to_phone = schedule.team_member.phone

        # Send with retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                # Apply exponential backoff (except first attempt)
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))
                    logger.info(
                        f"Retry attempt {attempt + 1}/{self.max_retries} "
                        f"for schedule {schedule.id} after {delay}s delay"
                    )
                    sleep(delay)

                # Send SMS
                result = self._send_sms(to_phone, message_body)

                # Log successful send with recipient snapshot
                _ = self.notification_repo.log_notification_attempt(
                    schedule_id=schedule.id,
                    status='sent',
                    twilio_sid=result['sid'],
                    error_message=None,
                    recipient_name=schedule.team_member.name,
                    recipient_phone=schedule.team_member.phone
                )

                # Mark schedule as notified
                schedule.notified = True
                schedule.notified_at = datetime.now()
                self.db.commit()

                logger.info(
                    f"SMS sent successfully to {self._sanitize_phone(to_phone)} "
                    f"for schedule {schedule.id} (SID: {result['sid']})"
                )

                return {
                    "success": True,
                    "schedule_id": schedule.id,
                    "twilio_sid": result['sid'],
                    "status": "sent",
                    "message": "SMS sent successfully",
                    "attempts": attempt + 1,
                    "error": None
                }

            except TwilioRestException as e:
                last_error = str(e)
                error_msg = f"Twilio error (attempt {attempt + 1}/{self.max_retries}): {str(e)}"
                logger.error(error_msg)

                # Log failed attempt
                self.notification_repo.log_notification_attempt(
                    schedule_id=schedule.id,
                    status='failed',
                    twilio_sid=None,
                    error_message=error_msg,
                    recipient_name=schedule.team_member.name,
                    recipient_phone=schedule.team_member.phone
                )

                # Check if error is retryable
                if not self._is_retryable_error(e):
                    logger.error(
                        f"Non-retryable Twilio error for schedule {schedule.id}: {str(e)}"
                    )
                    break

            except Exception as e:
                last_error = str(e)
                error_msg = f"Unexpected error (attempt {attempt + 1}/{self.max_retries}): {str(e)}"
                logger.error(error_msg)

                # Log failed attempt
                self.notification_repo.log_notification_attempt(
                    schedule_id=schedule.id,
                    status='failed',
                    twilio_sid=None,
                    error_message=error_msg,
                    recipient_name=schedule.team_member.name,
                    recipient_phone=schedule.team_member.phone
                )

        # All attempts failed
        logger.error(
            f"Failed to send SMS for schedule {schedule.id} after "
            f"{self.max_retries} attempts. Last error: {last_error}"
        )

        return {
            "success": False,
            "schedule_id": schedule.id,
            "twilio_sid": None,
            "status": "failed",
            "message": "Failed to send SMS after all retry attempts",
            "attempts": self.max_retries,
            "error": last_error
        }

    def _send_sms(self, to_phone: str, message_body: str) -> Dict[str, str]:
        """
        Send SMS via Twilio.

        Args:
            to_phone: Recipient phone number (E.164 format)
            message_body: SMS message text

        Returns:
            Dictionary with Twilio response data (sid, status)

        Raises:
            TwilioRestException: If Twilio API call fails
        """
        if self.mock_mode:
            # Mock mode for testing
            logger.info(f"[MOCK] Sending SMS to {to_phone}: {message_body}")
            return {
                "sid": f"SM{os.urandom(16).hex()}",
                "status": "sent"
            }

        message = self.twilio_client.messages.create(
            body=message_body,
            from_=self.from_phone,
            to=to_phone
        )

        return {
            "sid": message.sid,
            "status": message.status
        }

    def _compose_message(self, schedule: Schedule) -> str:
        """
        Compose SMS message for a schedule assignment.

        Format:
        "WhoseOnFirst: Your on-call shift has started.
        Duration: 24 hours (until Mon 08:00 AM)
        Questions? Contact admin."

        Args:
            schedule: Schedule instance

        Returns:
            Formatted SMS message text (under 160 characters)
        """
        member_name = schedule.team_member.name
        duration = schedule.shift.duration_hours
        end_time = schedule.end_datetime.strftime('%a %I:%M %p')

        message = (
            f"WhoseOnFirst: {member_name}, your on-call shift has started.\n"
            f"Duration: {duration}h (until {end_time})\n"
            f"Questions? Contact admin."
        )

        # Ensure message is under 160 characters for single SMS
        if len(message) > 160:
            # Truncate if too long
            message = message[:157] + "..."
            logger.warning(f"SMS message truncated to 160 characters for schedule {schedule.id}")

        return message

    def _is_retryable_error(self, error: TwilioRestException) -> bool:
        """
        Determine if a Twilio error is retryable.

        Retryable errors (temporary):
        - 429: Too Many Requests (rate limiting)
        - 500-503: Server errors
        - 20003: Authentication issues (temporary)
        - 21610: Message cannot be sent to this phone number (temporary)

        Non-retryable errors (permanent):
        - 21211: Invalid phone number
        - 21408: Permission denied
        - 21614: Invalid number format

        Args:
            error: TwilioRestException instance

        Returns:
            True if error is retryable, False otherwise
        """
        # HTTP status codes
        if hasattr(error, 'status'):
            if error.status in [429, 500, 502, 503]:
                return True

        # Twilio error codes
        if hasattr(error, 'code'):
            retryable_codes = [20003, 21610, 30001, 30002, 30003, 30004, 30005, 30006]
            non_retryable_codes = [21211, 21408, 21614, 21217, 21601]

            if error.code in non_retryable_codes:
                return False
            if error.code in retryable_codes:
                return True

        # Default to non-retryable for unknown errors
        return False

    def _sanitize_phone(self, phone: str) -> str:
        """
        Sanitize phone number for logging (mask last 4 digits).

        Args:
            phone: Phone number in E.164 format

        Returns:
            Sanitized phone number (e.g., +1555123XXXX)
        """
        if len(phone) >= 4:
            return phone[:-4] + 'XXXX'
        return phone

    def send_batch_notifications(
        self,
        schedules: list[Schedule],
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Send notifications for multiple schedules.

        Args:
            schedules: List of Schedule instances
            force: If True, send even if already notified

        Returns:
            Dictionary with batch result summary:
            {
                "total": int,
                "successful": int,
                "failed": int,
                "skipped": int,
                "results": list of individual results
            }
        """
        results = []
        successful = 0
        failed = 0
        skipped = 0

        logger.info(f"Starting batch notification for {len(schedules)} schedules")

        for schedule in schedules:
            try:
                result = self.send_notification(schedule, force=force)
                results.append(result)

                if result['success']:
                    if result['status'] == 'skipped':
                        skipped += 1
                    else:
                        successful += 1
                else:
                    failed += 1

            except Exception as e:
                error_msg = f"Error sending notification for schedule {schedule.id}: {str(e)}"
                logger.error(error_msg)
                results.append({
                    "success": False,
                    "schedule_id": schedule.id,
                    "twilio_sid": None,
                    "status": "error",
                    "message": error_msg,
                    "attempts": 0,
                    "error": str(e)
                })
                failed += 1

        summary = {
            "total": len(schedules),
            "successful": successful,
            "failed": failed,
            "skipped": skipped,
            "results": results
        }

        logger.info(
            f"Batch notification complete: {successful} successful, "
            f"{failed} failed, {skipped} skipped out of {len(schedules)} total"
        )

        return summary

    def get_delivery_status(self, twilio_sid: str) -> Optional[Dict[str, Any]]:
        """
        Query Twilio for message delivery status.

        Useful for checking delivery confirmation after sending.

        Args:
            twilio_sid: Twilio message SID

        Returns:
            Dictionary with status information or None if not found

        Raises:
            TwilioRestException: If Twilio API call fails
        """
        if self.mock_mode:
            return {
                "sid": twilio_sid,
                "status": "delivered",
                "error_code": None,
                "error_message": None
            }

        try:
            message = self.twilio_client.messages(twilio_sid).fetch()
            return {
                "sid": message.sid,
                "status": message.status,
                "error_code": message.error_code,
                "error_message": message.error_message
            }
        except TwilioRestException as e:
            logger.error(f"Failed to fetch message status for SID {twilio_sid}: {str(e)}")
            return None
