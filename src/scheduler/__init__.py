"""
Scheduler Module

This module provides APScheduler integration for automated background jobs.
Currently implements daily SMS notifications at 8:00 AM CST.
"""

from src.scheduler.schedule_manager import (
    ScheduleManager,
    get_schedule_manager,
    send_daily_notifications,
    trigger_notifications_manually,
    trigger_weekly_summary_manually,
    check_auto_renewal,
    complete_past_overrides,
    trigger_override_completion_manually
)

__all__ = [
    'ScheduleManager',
    'get_schedule_manager',
    'send_daily_notifications',
    'trigger_notifications_manually',
    'trigger_weekly_summary_manually',
    'check_auto_renewal',
    'complete_past_overrides',
    'trigger_override_completion_manually'
]
