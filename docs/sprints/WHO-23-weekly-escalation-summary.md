# WHO-23: Weekly Escalation Contact Schedule Summary

**Sprint Plan - Weekly SMS to Fixed Escalation Contacts**

---

## Sprint Overview

**Linear Issue**: [WHO-23](https://linear.app/hextrackr/issue/WHO-23)
**Type**: Feature Enhancement (High Priority - Supervisor Request)
**Planned Version**: v1.3.0 (minor - new feature)
**Estimated Time**: 3-4 hours
**Approach**: Build on existing scheduler + SMS + settings patterns
**Status**: 📋 PLANNING (Not yet started)

---

## Problem Summary

Escalation contacts (Ken U, Steve N) need to know who is on-call each day when they receive escalation calls at odd hours, but don't need daily SMS notifications like primary on-call members.

**User Need:** *"When I get an escalation call at 2am, I need to quickly know who was supposed to be on-call that day without logging into the dashboard."*

**Current Workarounds:**
- Must log into dashboard to view weekly calendar
- No offline/quick reference available during emergencies
- Escalation contacts are "in the dark" about rotation schedule

---

## Proposed Solution

Send automated weekly SMS summary to both escalation contacts (primary + secondary phones) every Monday at 8:00 AM CST with upcoming 7-day schedule.

**Key Features:**
- Weekly SMS sent Monday 8:00 AM CST (new APScheduler job)
- Lists 7 days (Mon-Sun) with team member name + primary phone
- 48-hour shifts display as "(48h)" on first day, "(continues)" on second
- Toggle enable/disable via Settings
- Manual trigger endpoint for testing
- Customizable template (future enhancement)

---

## Research Phase (CURRENT)

### Existing Patterns to Leverage

**Pattern 1: APScheduler Jobs** (WHO-2 Auto-Renewal)
- Daily job at 2:00 AM CST for auto-renewal check
- File: `src/scheduler/schedule_manager.py`
- Need to explore: Job registration, timezone handling, error handling

**Pattern 2: Settings System** (WHO-2 Auto-Renewal, WHO-20 SMS Template)
- Settings table with typed values (bool, int, str, float)
- Frontend toggle with load/save logic
- Files: `src/models/settings.py`, `src/services/settings_service.py`, `src/api/routes/settings.py`

**Pattern 3: SMS Service** (WHO-17 Dual-Device)
- Concurrent SMS to multiple phones
- Retry logic with exponential backoff
- Notification logging with categories
- File: `src/services/sms_service.py`

**Pattern 4: Notification Logging**
- Category-based logging (e.g., `daily`, `manual`, `escalation_weekly`)
- Snapshot recipient data at send time
- File: `src/repositories/notification_log_repository.py`

### Research Questions to Answer

**Scheduler:**
- [ ] How are APScheduler jobs registered in `schedule_manager.py`?
- [ ] How does timezone handling work (America/Chicago)?
- [ ] What's the error handling pattern for scheduled jobs?
- [ ] How do we prevent duplicate job registration?

**SMS Service:**
- [ ] How do we send to multiple recipients concurrently?
- [ ] What's the message composition pattern?
- [ ] How do we handle retry logic for weekly sends?
- [ ] Where do we get escalation contact phone numbers?

**Settings:**
- [ ] What's the pattern for boolean toggles (enabled/disabled)?
- [ ] How do we lazy-initialize default settings?
- [ ] What's the API endpoint pattern for settings CRUD?
- [ ] How does frontend load/save settings?

**Schedule Queries:**
- [ ] How do we query "next 7 days starting Monday"?
- [ ] How do we handle 48-hour shifts in message formatting?
- [ ] What if schedule doesn't cover full 7 days?

---

## Plan Phase (PENDING)

### Implementation Breakdown

**Phase 1: Research** (✅ CURRENT)
- Explore existing scheduler, SMS, settings patterns
- Document file:line references for key code
- Identify reusable functions vs. new code needed

**Phase 2: Plan** (PENDING)
- Design database changes (settings keys)
- Design new scheduler job function
- Design SMS message format
- Design API endpoints
- Design frontend UI (toggle + test button)
- Break into 5-10 implementation tasks

**Phase 3: Implement** (TOMORROW)
- Execute tasks from plan
- Test with manual trigger
- Verify notification logging
- Docker rebuild + testing
- Update CHANGELOG.md
- Bump version to v1.3.0

---

## Expected SMS Message Format

```
WhoseOnFirst Weekly Schedule (Nov 25 - Dec 1)

Mon 11/25: Lance B +19187019714
Tue 11/26: Gary K +19187019714 (48h)
Wed 11/27: Gary K (continues)
Thu 11/28: Troy M +19187019714
Fri 11/29: Mike P +19187019714
Sat 11/30: Travis H +19187019714
Sun 12/01: Gerald S +19187019714

Questions? Reply to this message.
```

**Character Count:** ~320 chars (2 SMS segments @ $0.008/segment = $0.016)
**Recipients:** 2 (Ken U + Steve N, both with primary + secondary phones = 4 total)
**Weekly Cost:** ~$0.064/week (~$3.33/year)

---

## Success Criteria

- [ ] New setting: `escalation_weekly_enabled` (default: False)
- [ ] New APScheduler job runs every Monday 8:00 AM CST
- [ ] SMS sent to both escalation contacts (all configured phones)
- [ ] Message lists 7 days with correct formatting
- [ ] 48-hour shifts display correctly ("(48h)" and "(continues)")
- [ ] Manual trigger endpoint works for testing
- [ ] Notification log entries created with category `escalation_weekly`
- [ ] Frontend toggle enable/disable persists
- [ ] Frontend "Send Test" button triggers immediate send

---

## Files to Modify (TBD - Research Phase)

**Backend:**
- `src/scheduler/schedule_manager.py` - New weekly job
- `src/services/sms_service.py` - New method for weekly summary
- `src/services/settings_service.py` - New setting methods
- `src/api/routes/settings.py` - New endpoints (optional)
- `src/repositories/schedule_repository.py` - Query for next 7 days

**Frontend:**
- `frontend/settings.html` OR `frontend/notifications.html` - Toggle UI + test button

**Database:**
- No migration needed (uses existing `settings` table)

---

## Rollback Plan

- Setting defaults to `False` - no impact if disabled
- Can toggle off via frontend if issues arise
- Manual trigger allows testing before enabling scheduled job
- Notification log preserves history even if feature disabled

---

## Notes

**Sprint Created**: 2025-11-21 22:00 CST
**Status**: ✅ PLANNING COMPLETE (Ready for Implementation)
**Next Session**: Implementation (Tomorrow)

**Session Goals for Tonight:**
1. ✅ Create sprint file with v1.3.0 planned version
2. ✅ Research existing patterns (scheduler, SMS, settings, schedule queries)
3. ✅ Document file:line references for key code (all research findings documented)
4. ✅ Plan implementation steps with task breakdown (7 phases, 15 tasks, 3-4 hours)
5. ✅ COMPLETE - Ready for implementation tomorrow!

**Session Goals for Tomorrow:**
1. Review tonight's research and plan
2. Execute implementation tasks
3. Test with manual trigger
4. Update CHANGELOG and version to v1.3.0
5. Close out sprint file

---

## Research Findings (✅ COMPLETED)

### Scheduler Patterns

**File:** `src/scheduler/schedule_manager.py`

**Key Pattern: CronTrigger for Weekly Job** (lines 83-112)
```python
# Pattern for adding weekly job (Monday 8:00 AM)
self.scheduler.add_job(
    func=send_weekly_escalation_summary,  # New function to create
    trigger=CronTrigger(day_of_week='mon', hour=8, minute=0, timezone=CHICAGO_TZ),
    id='weekly_escalation_summary',
    name='Weekly Escalation Contact Schedule Summary',
    replace_existing=True
)
```

**Key Pattern: Database Session Context Manager** (lines 213-227)
```python
@contextmanager
def get_db_session():
    """Thread-safe DB session for background jobs"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in job function:
with get_db_session() as db:
    try:
        settings_service = SettingsService(db)
        # ... job logic
    except Exception as e:
        logger.error("Error: %s", str(e), exc_info=True)
        raise
```

**Key Pattern: Manual Trigger Wrapper** (lines 299-335)
```python
def trigger_weekly_summary_manually() -> dict:
    """API-callable wrapper for scheduled function"""
    try:
        result = send_weekly_escalation_summary()
        return {
            'status': 'success',
            'message': 'Weekly summary sent',
            'timestamp': datetime.now(CHICAGO_TZ).isoformat(),
            'successful': result['successful'],
            'failed': result['failed']
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

**Reusable Functions:**
- `get_db_session()` - Context manager for thread-safe DB access
- Pattern: Job function + manual trigger wrapper for testing

---

### SMS Service Patterns

**File:** `src/services/sms_service.py`

**Key Pattern: Send to Multiple Recipients** (lines 190-245)
```python
# Current pattern sends to primary + secondary phones for ONE person
# We need to adapt this to send to MULTIPLE people (2 escalation contacts)
# Each contact has primary + secondary phone = 4 total SMS sends

# Pattern to adapt:
primary_result = self._send_to_single_phone(
    phone=schedule.team_member.phone,
    message_body=message_body,
    schedule=schedule,
    phone_type="primary"
)

secondary_result = self._send_to_single_phone(
    phone=schedule.team_member.secondary_phone,
    message_body=message_body,
    schedule=schedule,
    phone_type="secondary"
)
```

**Key Pattern: Manual Notification with Category** (lines 566-684)
```python
# Send custom message without schedule_id (manual/ad-hoc notifications)
result = service.send_manual_notification(
    team_member=member,
    message="Custom message here"
)

# Logs with schedule_id=NULL for manual sends
# We'll use this pattern but add category='escalation_weekly'
```

**Key Pattern: Message Composition** (lines 390-441)
```python
def _compose_message(self, schedule: Schedule) -> str:
    """Load template and format with variables"""
    template = self.settings_service.get_sms_template()
    message = template.format(
        name=member_name,
        start_time=start_time,
        end_time=end_time,
        duration=f"{duration_hours}h"
    )
    return message
```

**Notification Logging Pattern** (lines 282-289)
```python
# Always log with recipient snapshot data
log_entry = self.notification_repo.log_notification_attempt(
    schedule_id=schedule.id,  # Or NULL for manual
    status='sent',  # Or 'failed'
    twilio_sid=result['sid'],
    error_message=None,
    recipient_name=schedule.team_member.name,
    recipient_phone=phone
)
```

**Reusable Functions:**
- `_send_to_single_phone()` - Send with retry logic
- `_send_sms()` - Low-level Twilio call
- `_sanitize_phone()` - Mask for logging

**New Function Needed:**
- `send_weekly_escalation_summary()` - New method to send to multiple escalation contacts

---

### Settings System Patterns

**File:** `src/services/settings_service.py`

**GREAT NEWS:** Escalation contact config already exists! (lines 280-372)

**Existing Settings:**
```python
# Lines 14-23 - Setting key constants
ESCALATION_ENABLED = "escalation_enabled"
ESCALATION_PRIMARY_NAME = "escalation_primary_name"
ESCALATION_PRIMARY_PHONE = "escalation_primary_phone"
ESCALATION_SECONDARY_NAME = "escalation_secondary_name"
ESCALATION_SECONDARY_PHONE = "escalation_secondary_phone"

# Existing method (lines 281-301)
def get_escalation_config(self) -> Dict[str, Any]:
    return {
        "enabled": self.repository.get_value(ESCALATION_ENABLED, default=False),
        "primary_name": self.repository.get_value(ESCALATION_PRIMARY_NAME, default=None),
        "primary_phone": self.repository.get_value(ESCALATION_PRIMARY_PHONE, default=None),
        "secondary_name": self.repository.get_value(ESCALATION_SECONDARY_NAME, default=None),
        "secondary_phone": self.repository.get_value(ESCALATION_SECONDARY_PHONE, default=None)
    }
```

**Key Pattern: Boolean Toggle with Default** (lines 122-146)
```python
# Pattern for enable/disable toggle
def is_auto_renew_enabled(self) -> bool:
    return self.repository.get_value(AUTO_RENEW_ENABLED, default=True)

def set_auto_renew_enabled(self, enabled: bool) -> Settings:
    return self.set_setting(
        AUTO_RENEW_ENABLED,
        enabled,
        "bool",
        "Description here"
    )
```

**Key Pattern: Lazy Initialization** (lines 237-254)
```python
# SMS template auto-seeds default on first access
template = self.repository.get_value(SMS_TEMPLATE, default=None)
if template is None:
    self.set_sms_template(DEFAULT_SMS_TEMPLATE)
    template = DEFAULT_SMS_TEMPLATE
return template
```

**New Settings Needed:**
```python
# Add to constants (line 24):
ESCALATION_WEEKLY_ENABLED = "escalation_weekly_enabled"

# New methods to add:
def is_escalation_weekly_enabled(self) -> bool:
    return self.repository.get_value(ESCALATION_WEEKLY_ENABLED, default=False)

def set_escalation_weekly_enabled(self, enabled: bool) -> Settings:
    return self.set_setting(
        ESCALATION_WEEKLY_ENABLED,
        enabled,
        "bool",
        "Send weekly SMS schedule summary to escalation contacts every Monday 8:00 AM"
    )
```

**Reusable Functions:**
- `get_escalation_config()` - Already exists! Returns all escalation contact info
- `set_setting()` - Generic setting storage with type auto-detection

---

### Schedule Query Patterns

**File:** `src/repositories/schedule_repository.py`

**Key Pattern: Date Range Query** (lines 42-84)
```python
def get_by_date_range(
    self,
    start_date: datetime,
    end_date: datetime,
    include_relationships: bool = True
) -> List[Schedule]:
    # Convert timezone-aware to naive for SQLite comparison
    start_naive = start_date.replace(tzinfo=None) if start_date.tzinfo else start_date
    end_naive = end_date.replace(tzinfo=None) if end_date.tzinfo else end_date

    query = self.db.query(self.model).filter(
        and_(
            self.model.start_datetime >= start_naive,
            self.model.start_datetime <= end_naive
        )
    )

    if include_relationships:
        query = query.options(
            joinedload(self.model.team_member),
            joinedload(self.model.shift)
        )

    return query.order_by(self.model.start_datetime).all()
```

**Usage for Next 7 Days (Starting Monday):**
```python
# Get upcoming Monday 00:00:00
from datetime import datetime, timedelta
from pytz import timezone

chicago_tz = timezone('America/Chicago')
now = datetime.now(chicago_tz)

# Find next Monday (or today if already Monday)
days_until_monday = (7 - now.weekday()) % 7
if days_until_monday == 0 and now.hour >= 8:  # Already sent today
    days_until_monday = 7  # Next Monday

next_monday = (now + timedelta(days=days_until_monday)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
following_sunday = next_monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

# Query schedules
schedules = schedule_repo.get_by_date_range(
    start_date=next_monday,
    end_date=following_sunday,
    include_relationships=True
)
```

**Key Pattern: Eager Loading** (lines 74-78)
```python
# Always load relationships for display
query = query.options(
    joinedload(self.model.team_member),
    joinedload(self.model.shift)
)
```

**Reusable Functions:**
- `get_by_date_range()` - Perfect for querying next 7 days
- Handles timezone conversion for SQLite compatibility

---

### Research Questions - ANSWERED ✅

**Scheduler:**
- ✅ How are jobs registered? → `scheduler.add_job()` with CronTrigger (lines 83-112)
- ✅ Timezone handling? → `CHICAGO_TZ` constant, passed to CronTrigger (line 88)
- ✅ Error handling? → Try/except with logger.error in job function (lines 400+)
- ✅ Prevent duplicate registration? → `replace_existing=True` parameter (line 111)

**SMS Service:**
- ✅ Send to multiple recipients? → Loop through contacts, call `_send_to_single_phone()` for each
- ✅ Message composition? → Create new method similar to `_compose_message()` (lines 390-441)
- ✅ Retry logic? → Built into `_send_to_single_phone()` with exponential backoff (lines 247-355)
- ✅ Get escalation contacts? → `settings_service.get_escalation_config()` (lines 281-301)

**Settings:**
- ✅ Boolean toggles? → `get_value()` with default, `set_setting()` with type "bool" (lines 122-146)
- ✅ Lazy initialization? → Check if None, seed default on first access (lines 237-254)
- ✅ API endpoints? → Reuse existing `/settings/` routes, add new methods
- ✅ Frontend load/save? → Existing settings.html or notifications.html UI patterns

**Schedule Queries:**
- ✅ Query next 7 days? → `get_by_date_range()` with Monday-Sunday range (lines 42-84)
- ✅ Handle 48h shifts? → Check `shift.duration_hours`, format message accordingly
- ✅ Incomplete schedule? → Show available days, note gaps in message if needed

---

## Implementation Plan (✅ COMPLETED)

### Task Breakdown

**Phase 1: Settings Layer** (30 min)

**Task 1.1: Add Weekly Toggle Setting** [BACKEND - settings_service.py]
- File: `src/services/settings_service.py`
- Add constant `ESCALATION_WEEKLY_ENABLED = "escalation_weekly_enabled"` (after line 23)
- Add method `is_escalation_weekly_enabled()` returning bool, default=False
- Add method `set_escalation_weekly_enabled(enabled: bool)` with description
- Pattern: Copy from `is_auto_renew_enabled()` / `set_auto_renew_enabled()` (lines 122-146)

---

**Phase 2: SMS Service Layer** (45 min)

**Task 2.1: Add Weekly Summary Composition Method** [BACKEND - sms_service.py]
- File: `src/services/sms_service.py`
- Add new method `_compose_weekly_summary(schedules: List[Schedule]) -> str`
- Input: List of 7 schedules (Mon-Sun)
- Output: Formatted message like:
  ```
  WhoseOnFirst Weekly Schedule (Nov 25 - Dec 1)

  Mon 11/25: Lance B +19187019714
  Tue 11/26: Gary K +19187019714 (48h)
  Wed 11/27: Gary K (continues)
  Thu 11/28: Troy M +19187019714
  ...
  ```
- Handle 48h shifts: First day shows "(48h)", second day shows "(continues)" without phone
- Handle gaps: Show "No assignment" if missing
- Group consecutive schedules by team_member_id to detect 48h shifts
- Location: After `_compose_message()` method (after line 441)

**Task 2.2: Add Send to Escalation Contacts Method** [BACKEND - sms_service.py]
- File: `src/services/sms_service.py`
- Add new method `send_escalation_weekly_summary(message: str, escalation_config: dict) -> dict`
- Get escalation contacts from config:
  ```python
  primary_name = escalation_config.get('primary_name')
  primary_phone = escalation_config.get('primary_phone')
  secondary_name = escalation_config.get('secondary_name')
  secondary_phone = escalation_config.get('secondary_phone')
  ```
- Send to each phone using `_send_sms()` directly (not tied to schedule)
- Log each send with `notification_repo.log_notification_attempt()`:
  - `schedule_id=None` (manual/weekly notification)
  - `status='sent'` or `'failed'`
  - `recipient_name=contact_name`
  - `recipient_phone=contact_phone`
  - Add `category='escalation_weekly'` if notification log supports categories
- Return summary dict: `{'successful': int, 'failed': int, 'total': int}`
- Location: After `send_manual_notification()` method (after line 684)

---

**Phase 3: Scheduler Layer** (60 min)

**Task 3.1: Create Weekly Summary Scheduled Job Function** [BACKEND - schedule_manager.py]
- File: `src/scheduler/schedule_manager.py`
- Add new function `send_weekly_escalation_summary() -> dict` (module-level, after line 439)
- Pattern: Copy from `check_auto_renewal()` structure (lines 338-439)
- Logic:
  1. Use `get_db_session()` context manager
  2. Check if feature enabled via `settings_service.is_escalation_weekly_enabled()`
  3. Get escalation config via `settings_service.get_escalation_config()`
  4. Validate at least one contact has name+phone configured
  5. Calculate next Monday 00:00 to following Sunday 23:59 (America/Chicago)
  6. Query schedules via `schedule_repo.get_by_date_range()`
  7. Compose weekly summary message via `sms_service._compose_weekly_summary()`
  8. Send to escalation contacts via `sms_service.send_escalation_weekly_summary()`
  9. Return summary dict with successful/failed counts
- Error handling: Try/except with logger.error, re-raise exception
- Location: After `check_auto_renewal()` (after line 439)

**Task 3.2: Add Manual Trigger Wrapper** [BACKEND - schedule_manager.py]
- File: `src/scheduler/schedule_manager.py`
- Add new function `trigger_weekly_summary_manually() -> dict` (after Task 3.1 function)
- Pattern: Copy from `trigger_notifications_manually()` (lines 299-335)
- Call `send_weekly_escalation_summary()`, wrap result in API-friendly dict
- Return `{'status': 'success', 'successful': X, 'failed': Y, 'timestamp': ...}` or error dict
- Location: After `send_weekly_escalation_summary()` function

**Task 3.3: Register Weekly Job in Scheduler** [BACKEND - schedule_manager.py]
- File: `src/scheduler/schedule_manager.py`
- Add new method `add_weekly_escalation_job(self)` to `ScheduleManager` class
- Pattern: Copy from `add_auto_renewal_job()` (lines 83-112)
- Use `CronTrigger(day_of_week='mon', hour=8, minute=0, timezone=CHICAGO_TZ)`
- Job ID: `'weekly_escalation_summary'`
- Job name: `'Weekly Escalation Contact Schedule Summary'`
- `replace_existing=True`
- Location: After `add_auto_renewal_job()` method (after line 112)

**Task 3.4: Call Registration in Scheduler Start** [BACKEND - schedule_manager.py]
- File: `src/scheduler/schedule_manager.py`
- In `start()` method, add call to `self.add_weekly_escalation_job()` (after line 140)
- Pattern: Same as `self.add_auto_renewal_job()` call (line 139)

---

**Phase 4: API Layer** (30 min)

**Task 4.1: Add Manual Trigger API Endpoint** [BACKEND - settings.py or schedules.py]
- File: `src/api/routes/schedules.py` (add to schedules since it's notification-related)
- Add new POST endpoint `/api/v1/schedules/notifications/weekly-summary/trigger`
- Pattern: Copy from `/notifications/trigger` endpoint structure
- Call `trigger_weekly_summary_manually()` from schedule_manager
- Return API response with result
- Location: After existing notification trigger endpoint

**Task 4.2: Add Settings API Endpoints (Optional)** [BACKEND - settings.py]
- File: `src/api/routes/settings.py`
- If needed, add GET/PUT endpoints for escalation weekly toggle
- May not be needed if frontend uses generic settings endpoints
- Decision: Check if existing settings endpoints support generic key/value updates

---

**Phase 5: Frontend Layer** (45 min)

**Task 5.1: Add Weekly Summary Toggle UI** [FRONTEND - notifications.html]
- File: `frontend/notifications.html`
- Add new card section: "Weekly Escalation Contact Summary"
- UI elements:
  - Toggle switch for enable/disable (id: `escalationWeeklyEnabled`)
  - Info text: "Send weekly schedule summary every Monday 8:00 AM CST"
  - "Send Test Now" button (id: `sendWeeklyTestBtn`)
  - Status message area for test result
- Pattern: Copy from auto-renewal toggle UI structure
- Location: After existing notification settings sections

**Task 5.2: Add Frontend JavaScript Logic** [FRONTEND - notifications.html]
- File: `frontend/notifications.html` (inline JS section)
- On page load:
  1. Fetch escalation config from `/api/v1/settings/` or specific endpoint
  2. Check if `escalation_weekly_enabled` exists, populate toggle
  3. If no escalation contacts configured, disable toggle + show warning
- On toggle change:
  1. Call settings API to update `escalation_weekly_enabled`
  2. Show success/error toast
- On "Send Test Now" click:
  1. Call `/api/v1/schedules/notifications/weekly-summary/trigger`
  2. Show loading spinner
  3. Display result (success count, failed count) in status area
  4. Show toast with summary
- Pattern: Copy from existing settings save/load logic

---

**Phase 6: Testing & Docker** (30 min)

**Task 6.1: Docker Rebuild & Verification** [DEPLOYMENT]
- Rebuild Docker dev container: `docker-compose -f docker-compose.dev.yml down && build && up -d`
- Verify scheduler registration: Check logs for "Weekly Escalation Contact Schedule Summary" job added
- Check no startup errors related to new code

**Task 6.2: Manual Testing** [TESTING]
- Navigate to Notifications page
- Verify toggle appears with correct state
- Enable weekly summary, verify saves
- Click "Send Test Now", verify:
  - API call succeeds
  - 4 SMS sent (2 contacts × 2 phones each) OR shows error if Twilio not configured
  - Notification log entries created with NULL schedule_id
  - Message format matches expected format (7 days, 48h handling)
- Check Docker logs for job execution logging
- Verify no errors in browser console

**Task 6.3: Notification Log Verification** [TESTING]
- Query notification_log table: `SELECT * FROM notification_log WHERE schedule_id IS NULL ORDER BY sent_at DESC LIMIT 10`
- Verify entries have:
  - Correct recipient names (Ken U, Steve N)
  - Correct recipient phones
  - Status 'sent' (or 'failed' if expected)
  - Twilio SID populated (if sent successfully)

---

### Implementation Order (Tomorrow's Session)

1. ✅ **Settings** → Task 1.1 (fastest, enables feature flag)
2. ✅ **SMS Service** → Tasks 2.1, 2.2 (message logic + sending)
3. ✅ **Scheduler** → Tasks 3.1, 3.2, 3.3, 3.4 (background job setup)
4. ✅ **API** → Tasks 4.1, 4.2 (expose manual trigger)
5. ✅ **Frontend** → Tasks 5.1, 5.2 (UI for control)
6. ✅ **Docker Rebuild** → Task 6.1 (rebuild container)
7. ✅ **Testing** → Tasks 6.2, 6.3 (verify everything works)

**Total Estimated Time:** 3-4 hours (includes testing + debugging)

---

### Testing Checklist

**Pre-Implementation Testing:**
- [x] Research verified existing patterns work correctly
- [x] Escalation config already exists and returns expected data

**Unit Testing (Optional - Time Permitting):**
- [ ] Test `_compose_weekly_summary()` with various schedule scenarios:
  - Full 7-day week with no gaps
  - Week with 48h shift (Tue-Wed)
  - Week with missing days
  - Week with multiple 48h shifts
- [ ] Test `send_weekly_escalation_summary()` with mock Twilio
- [ ] Test scheduler job registration (verify cron expression)

**Integration Testing (Manual - REQUIRED):**
- [ ] **Settings Layer**
  - [ ] `is_escalation_weekly_enabled()` returns False by default
  - [ ] `set_escalation_weekly_enabled(True)` persists to database
  - [ ] Toggle can be disabled again
- [ ] **Scheduler Layer**
  - [ ] Weekly job registered on scheduler start (check logs)
  - [ ] Manual trigger wrapper returns success dict
  - [ ] Manual trigger with feature disabled returns early (no SMS sent)
  - [ ] Manual trigger with no escalation contacts configured returns error
- [ ] **SMS Service Layer**
  - [ ] Message composition formats 7 days correctly
  - [ ] 48h shifts show "(48h)" and "(continues)" correctly
  - [ ] Phone numbers formatted correctly in message
  - [ ] Missing days show "No assignment" or similar
- [ ] **Notification Logging**
  - [ ] Entries created with `schedule_id=NULL`
  - [ ] Recipient name and phone captured correctly
  - [ ] Status 'sent' or 'failed' logged correctly
  - [ ] Twilio SID populated for successful sends
- [ ] **Frontend UI**
  - [ ] Toggle reflects current database state on load
  - [ ] Toggle changes save successfully
  - [ ] "Send Test Now" button triggers manual send
  - [ ] Status message shows send results (successful/failed counts)
  - [ ] Warning shown if no escalation contacts configured
- [ ] **End-to-End**
  - [ ] Enable feature, click "Send Test Now"
  - [ ] Verify 4 SMS sent (or 2 if secondary phones not configured)
  - [ ] Verify message format matches expected (7 days, correct dates)
  - [ ] Verify notification log has 4 entries with correct data
  - [ ] Check actual SMS received (if Twilio configured)
  - [ ] Verify Docker logs show successful execution

**Docker Testing:**
- [ ] Container rebuilds without errors
- [ ] Scheduler starts and registers weekly job
- [ ] No errors in `docker-compose -f docker-compose.dev.yml logs -f`
- [ ] API endpoints accessible at http://localhost:8900
- [ ] Frontend loads correctly with new UI elements

**Edge Cases:**
- [ ] Feature disabled → Manual trigger returns early, no SMS sent
- [ ] No escalation contacts configured → Error message, no SMS sent
- [ ] Only primary contact configured → 2 SMS sent (primary + secondary_phone)
- [ ] Schedule doesn't cover full 7 days → Message shows gaps correctly
- [ ] 48h shift at end of week (Sat-Sun) → Formatting correct
- [ ] Twilio API failure → Retry logic works, logged correctly
- [ ] Multiple consecutive 48h shifts → All formatted correctly

**Regression Testing:**
- [ ] Existing daily notifications still work
- [ ] Auto-renewal still works (if enabled)
- [ ] Escalation display on dashboard unchanged
- [ ] Other settings still load/save correctly

---

**Sprint Status**: 📋 PLANNING COMPLETE - Ready for Implementation (Tomorrow)
