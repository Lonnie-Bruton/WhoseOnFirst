# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WhoseOnFirst is an automated on-call rotation and SMS notification system for technical teams. The system ensures fair shift distribution using a simple circular rotation algorithm, schedules the double-shift during the workweek (Tue-Wed) to minimize weekend impact, and automatically notifies on-call personnel at 8:00 AM CST via Twilio.

**Current Status (2025-11-09):** Phase 1 MVP COMPLETE ✅
- Backend: 100% complete (FastAPI/APScheduler/Twilio)
- Frontend: 100% complete (5 pages, full CRUD, live data integration)
- Testing: 288 tests passing, 85% coverage
- **Blocker:** Awaiting Twilio US number approval (~1 week)
- **Next:** Phase 2 - Docker/Podman offline installer + Authentication

**Target Deployment:** RHEL 10 VM via Docker/Podman, with development/testing on macOS + Proxmox RHEL lab.

## Core Architecture Principles

### Layered Architecture (docs/planning/architecture.md)

The application follows a strict layered architecture with dependency injection:

1. **API Layer** (FastAPI routes) - HTTP handling, validation, serialization
2. **Service Layer** - Business logic, coordinates between API and data layers
3. **Data Access Layer** (Repository Pattern) - SQLAlchemy ORM operations
4. **Background Scheduler** (APScheduler) - Daily SMS job at 8:00 AM CST

**Critical:** Services should never call other services directly for data operations. Use repositories for all database access.

### Circular Rotation Algorithm (✅ IMPLEMENTED)

The rotation algorithm in `src/services/rotation_algorithm.py` implements:
- **Simple circular rotation:** Each week, person on Shift N moves to Shift N+1
- **Modulo wrapping:** `member_index = (shift_index + week_offset) % team_size`
- **No special weekend logic:** The 48-hour double shift (Tue-Wed) naturally distributes workload fairly
- **Works with any team size:** From 1 member to 15+ members
- **Timezone-aware:** All datetimes use America/Chicago timezone
- **100% test coverage:** 30 comprehensive tests covering all scenarios

See `src/services/rotation_algorithm.py` for implementation details.

## Technology Stack

**Backend:**
- FastAPI 0.115.0+ (async/await, automatic OpenAPI docs)
- Uvicorn 0.30.1+ (ASGI server, 2 workers in production)
- SQLAlchemy 2.0.31+ (ORM with async support)
- APScheduler 3.10.4+ (background jobs with America/Chicago timezone)
- Twilio Python SDK 9.2.3+ (SMS delivery)
- Pydantic 2.8.2+ (validation and serialization)

**Database:**
- Phase 1: SQLite (file-based, `./data/whoseonfirst.db`)
- Phase 2+: PostgreSQL (migration path via SQLAlchemy abstraction)

**Frontend:**
- Tabler.io 1.0.0-beta20 (Bootstrap 5 based admin framework)
- Vanilla JavaScript (no build step required)
- Fetch API for backend communication
- 16-color WCAG AA compliant team member color system

## Development Commands

### Setup and Running
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage (target: 80%+)
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_rotation_algorithm.py -v
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

### Database Management
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Docker Operations
```bash
# Build image
docker build -t whoseonfirst:latest .

# Run container
docker run -d --name whoseonfirst \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  whoseonfirst:latest

# View logs
docker logs -f whoseonfirst
```

## Critical Implementation Details

### Database Schema

See architecture.md lines 495-554 for full DDL. Key tables:

- **team_members:** id, name, phone (unique, E.164 format), is_active, **rotation_order** (for drag-drop ordering)
- **shifts:** id, shift_number (1-6), day_of_week, duration_hours (24 or 48), start_time
- **schedule:** id, team_member_id (FK), shift_id (FK), week_number, start_datetime, end_datetime, notified
- **notification_log:** id, schedule_id (FK), sent_at, status, twilio_sid, error_message

**Important indexes:** Create indexes on `schedule(start_datetime)`, `schedule(notified, start_datetime)`, and `team_members(is_active)` for query performance.

### API Endpoint Structure

All APIs under `/api/v1/` prefix:

- `/team-members/` - CRUD operations for team members
  - `PUT /reorder` - Bulk update rotation_order (drag-drop)
  - `DELETE /{id}/permanent` - Hard delete (requires name confirmation)
  - `POST /{id}/activate` - Reactivate deactivated member
- `/shifts/` - Shift configuration management
- `/schedules/` - Schedule generation, viewing, queries
  - `GET /current` - Current week
  - `GET /upcoming?weeks=X` - Upcoming schedules (1-104 weeks)
  - `GET /` - Query by date range
  - `GET /member/{id}` - Member-specific schedules
  - `GET /member/{id}/next` - Next assignment for member
  - `POST /generate` - Generate schedules (with force option)
  - `POST /regenerate` - Regenerate from date forward
  - `POST /notifications/trigger` - Manual SMS trigger
  - `GET /notifications/status` - Scheduler job status
- `/notifications/` - Notification history and logs

**Request Validation:** Use Pydantic models for all request/response schemas. Phone numbers must be validated to E.164 format (+1XXXXXXXXXX).

### APScheduler Configuration

```python
# Critical: Use America/Chicago timezone
from pytz import timezone

scheduler = BackgroundScheduler(
    jobstores={'default': SQLAlchemyJobStore(url=database_url)},
    timezone=timezone('America/Chicago')
)

# Daily notification job at 8:00 AM CST
scheduler.add_job(
    func=send_daily_notifications,
    trigger=CronTrigger(hour=8, minute=0),
    id='daily_oncall_sms',
    replace_existing=True,
    misfire_grace_time=300  # 5 minute grace period
)
```

**Important:** Scheduler must be started in FastAPI's lifespan context manager and gracefully shut down on application exit.

### Twilio Integration

```python
from twilio.rest import Client
import os

# Load from environment variables (never hardcode)
client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# SMS format (keep under 160 characters)
message = (
    f"WhoseOnFirst: Your on-call shift has started.\n"
    f"Duration: {duration_hours} hours (until {end_time})\n"
    f"Questions? Contact admin."
)
```

**Retry Logic:** Implement exponential backoff with 3 retry attempts using the `tenacity` library (see technical-stack.md lines 266-276).

**Logging:** Always log Twilio SID, status, and errors to `notification_log` table for audit trail.

## Security Requirements

- **Secrets Management:** All credentials in `.env` file, never committed to Git
- **Input Validation:** Pydantic validates all inputs; phone numbers must match E.164 regex: `^\+1\d{10}$`
- **SQL Injection Prevention:** Use SQLAlchemy ORM exclusively, no raw SQL
- **Phone Number Privacy:** Sanitize phone numbers in logs (mask last 4 digits)
- **HTTPS Only:** Enforce HTTPS in production via nginx reverse proxy

## Testing Requirements

- **Current Coverage:** 85% overall (288 tests), 100% for critical paths (rotation algorithm, SMS sending, scheduler)
- **Target:** Maintain 80%+ coverage as features are added
- **Test Structure:** Mirror `src/` directory structure in `tests/`
- **Critical Test Cases:**
  - Rotation algorithm circular rotation (multiple weeks, various team sizes, edge cases)
  - Schedule regeneration when team members added/removed
  - SMS retry logic on Twilio failures
  - Scheduler job execution at correct times
  - API endpoint validation (phone format, duplicate detection)

**Use pytest fixtures for:** Database sessions (rollback after each test), mock Twilio client, test data factories.

## Important Constraints

1. **Timezone Handling:** All times in America/Chicago (CST/CDT). Use `pytz` for timezone-aware datetimes. Never use naive datetimes.
2. **Phone Number Format:** E.164 standard only (+1XXXXXXXXXX). Validate on input, store consistently.
3. **Shift Configuration:** Default setup is 6 shifts with Shift 2 being the 48-hour double shift (Tue-Wed). Saturday = Shift 5, Sunday = Shift 6.
4. **Schedule Generation:** Generate minimum 4 weeks in advance. Regenerate from date of change when team composition changes.
5. **Database Transactions:** All write operations must be within explicit transactions with proper error handling and rollback.

## Common Pitfalls to Avoid

1. **Do not use system cron** - Use APScheduler for all scheduled tasks
2. **Do not hardcode timezones** - Always use `timezone('America/Chicago')` from pytz
3. **Do not skip phone validation** - Twilio will fail on invalid formats
4. **Do not forget indexes** - Query performance on `schedule` table depends on proper indexes
5. **Do not regenerate entire schedule** - Only regenerate from change date forward to preserve notification history
6. **Do not store secrets in code** - Use environment variables via python-dotenv

## Repository Pattern Example

```python
class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, data: dict):
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

# Specific repositories inherit from BaseRepository
class TeamMemberRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, TeamMember)

    def get_active(self):
        return self.db.query(self.model).filter(self.model.is_active == True).all()
```

## Service Layer Pattern Example

```python
class TeamMemberService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TeamMemberRepository(db)

    def create(self, member_data: TeamMemberCreate) -> TeamMember:
        # Validate phone uniqueness
        if self.repository.get_by_phone(member_data.phone):
            raise HTTPException(status_code=400, detail="Phone already exists")

        # Create member
        member = self.repository.create(member_data.dict())

        # Trigger schedule regeneration
        schedule_service = ScheduleService(self.db)
        schedule_service.regenerate_from_date(datetime.now())

        return member
```

## Documentation References

For detailed information, refer to these planning documents:

- **PRD.md** - Complete requirements, user stories, success metrics
- **architecture.md** - System design, data flow diagrams, component details
- **technical-stack.md** - Technology decisions, rationale, examples
- **research-notes.md** - Technology evaluation and trade-offs
- **DEVELOPMENT.md** - Day-to-day development workflows and commands

## Project Phases

### Phase 1: MVP (COMPLETE ✅)

**Backend:**
1. Team member management (CRUD with phone validation) ✅
2. Rotation order management (drag-drop, auto-assignment) ✅
3. Shift configuration (24h and 48h patterns) ✅
4. Schedule generation (circular rotation algorithm) ✅
5. Daily SMS notifications at 8:00 AM CST ✅
6. APScheduler integration with persistent job store ✅
7. Notification logging and audit trail ✅

**Frontend:**
1. Dashboard with live calendar and escalation chain ✅
2. Team member management UI with drag-drop reordering ✅
3. Shift configuration UI with weekly coverage timeline ✅
4. Schedule generation UI with 14-day preview ✅
5. Notifications history and SMS template editor ✅

### Phase 2: Deployment & Auth (IN PLANNING)

1. Docker/Podman containerization
2. Offline installer bundle (air-gapped deployment)
3. Authentication system
4. HTTPS support
5. Production deployment to RHEL 10 VM
6. Twilio 10DLC verification completion

### Phase 3: Enhancements (PLANNED)

1. Manual shift overrides (vacation/swap support)
2. Multi-level SMS notifications (Primary/Secondary/Tertiary)
3. Daily reminder for multi-day shifts (Day 2 of 48h shift)
4. Multiple contact methods per user (work phone + personal phone)
5. Auto-regeneration on configuration changes
6. Email notification backup (SendGrid/AWS SES/SMTP)
7. Enhanced reporting and analytics

### Phase 4: Advanced Features (FUTURE)

1. Multi-team support
2. PostgreSQL migration
3. Microsoft Teams/Slack integration
4. Mobile application (iOS + Android)
   - Push notifications via Firebase Cloud Messaging (FCM)
   - Enterprise deployment (no app store approval needed)
   - React Native or Flutter for cross-platform development
   - Rich notifications with schedule details and acknowledgment
   - Offline-first with sync capabilities
   - **Note:** Research session needed to evaluate frameworks, distribution methods, and cost-benefit vs SMS
5. REST API for external integrations
6. Extended shift types (8h, 12h, 3-7 day shifts, custom patterns)

**Intentionally Out of Scope:** PTO conflict detection, automated incident escalation, payment/compensation tracking, self-service shift swapping (requires auth).

## When Creating New Code

1. **Follow the layered architecture** - API → Service → Repository → Database
2. **Use type hints everywhere** - Enables IDE support and MyPy validation
3. **Write tests first** - Especially for rotation algorithm and critical paths
4. **Handle timezones explicitly** - Always use timezone-aware datetimes
5. **Log important events** - SMS sends, schedule changes, errors with context
6. **Document complex logic** - Especially rotation algorithm and schedule generation
7. **Validate all inputs** - Use Pydantic models with custom validators
8. **Use dependency injection** - FastAPI's `Depends()` for database sessions, services
