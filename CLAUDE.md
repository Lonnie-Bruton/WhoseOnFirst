# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start (30-Second Read)

**Project:** WhoseOnFirst - Automated on-call rotation and SMS notification system for 7-person technical team

**Current Status:** Phase 1 MVP Complete ✅ (v1.0.2 - Production Ready)
- Backend: 100% (FastAPI/APScheduler/Twilio)
- Frontend: 100% (8 pages with live data)
- Testing: 288 tests, 85% coverage
- Deployment: Docker containerized

**Blocker:** Twilio US number approval (~1 week wait)

**Next Phase:** Docker offline installer + Authentication system

**Work From:**
- **Linear Issues:** https://linear.app/hextrackr (Team: WhoseOnFirst)
- **Requirements:** `/docs/planning/PRD.md` (living document)
- **Code Patterns:** `/docs/reference/code-patterns.md`

**MCP Tool Priority:**
1. `memento` semantic_search - Find past decisions
2. `claude-context` search_code - Locate exact code
3. `sequential-thinking` - Break down problems
4. Manual file operations - Only after searches

---

## Documentation Hierarchy

```
LINEAR (Active Work)
  ↓ references
/docs/planning/PRD.md (Living Requirements)
  ↓ informs
CLAUDE.md (This File - AI Context)
  ↓ generates
CHANGELOG.md (Version History)
  ↓ summarizes
README.md (User-Facing)
```

**Full Documentation Guide:** `/docs/DOCUMENTATION_GUIDE.md`

---

## Project Architecture

### Core Principles

**Layered Architecture:**
```
API Layer (FastAPI routes)
  ↓
Service Layer (Business logic)
  ↓
Repository Layer (Data access)
  ↓
Database (SQLite → PostgreSQL path)
```

**Background Jobs:**
- APScheduler with America/Chicago timezone
- Daily SMS at 8:00 AM CST
- Auto-renewal check at 2:00 AM CST

**Circular Rotation Algorithm:**
- Simple modulo-based rotation: `member_index = shifts_elapsed % team_size`
- Works with any team size (1 to 15+ members)
- No special weekend logic (48h Tue-Wed shift naturally distributes workload)
- 100% test coverage (30 tests in `tests/test_rotation_algorithm.py`)

**Full Architecture:** `/docs/planning/architecture.md`

---

## Technology Stack

**Backend:**
- FastAPI 0.115+ (async, auto-docs)
- SQLAlchemy 2.0+ (ORM)
- APScheduler 3.10+ (background jobs)
- Twilio SDK 9.2+ (SMS)
- Uvicorn 0.30+ (ASGI server)

**Database:**
- Phase 1: SQLite (`./data/whoseonfirst.db`)
- Phase 2+: PostgreSQL migration path

**Frontend:**
- Tabler.io 1.0.0-beta20 (Bootstrap 5)
- Vanilla JavaScript (no build step)
- 16-color WCAG AA team member system

**Deployment:**
- Docker/Podman containers
- RHEL 10 target (production)
- macOS + Proxmox RHEL (dev/test)

**Full Stack Details:** `/docs/planning/technical-stack.md`

---

## Development Workflow

### Docker-First Development (PRIMARY)

**⚠️ IMPORTANT:** All development uses Docker containers to match production.

```bash
# Start dev container (port 8900)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Rebuild after code changes (REQUIRED)
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d

# Access application
# Web: http://localhost:8900
# API Docs: http://localhost:8900/docs
```

**Why Docker-first:**
- Matches production environment
- Avoids macOS SQLite corruption (uses named volume)
- No port conflicts (8900 dev vs 8000 prod)
- Database persists in `whoseonfirst-dev-db` volume

### Database Management

```bash
# Create migration (local with venv)
source venv/bin/activate
alembic revision --autogenerate -m "Description"

# Apply migrations (in Docker)
docker exec whoseonfirst-dev alembic upgrade head

# Backup database
docker cp whoseonfirst-dev:/app/data/whoseonfirst.db ./data/backup-$(date +%Y%m%d).db
```

### Testing (Local Environment)

```bash
# Activate venv
source venv/bin/activate

# Run all tests
pytest

# Run with coverage (target: 80%+)
pytest --cov=src --cov-report=html
```

**Full Workflow:** `/docs/RPI_PROCESS.md`

---

## Critical Implementation Details

### Database Schema

**Core Tables:**
- `team_members` - id, name, phone (unique E.164), is_active, **rotation_order**
- `shifts` - id, shift_number (1-6), day_of_week, duration_hours (24|48), start_time
- `schedule` - id, team_member_id (FK), shift_id (FK), week_number, start/end_datetime, notified
- `notification_log` - id, schedule_id (FK), sent_at, status, twilio_sid, error_message
- `settings` - id, key, value, value_type (for auto-renewal config)

**Important Indexes:** 
- `schedule(start_datetime)`, `schedule(notified, start_datetime)`, `team_members(is_active)`

**Full Schema DDL:** `/docs/planning/architecture.md` (lines 495-554)

### API Endpoint Structure

All APIs under `/api/v1/` prefix:

- `/team-members/` - CRUD, `/reorder` (drag-drop), `/{id}/permanent` (hard delete)
- `/shifts/` - Shift configuration management
- `/schedules/` - Generation, queries, notifications
  - `GET /current` - Current week
  - `GET /upcoming?weeks=X` - 1-104 weeks preview
  - `POST /generate` - Generate with force option
  - `POST /notifications/trigger` - Manual SMS
- `/settings/` - Auto-renewal configuration

**API Docs:** http://localhost:8900/docs (when running)

### Security Requirements

- **Secrets:** All credentials in `.env` file (never commit)
- **Validation:** Pydantic validates all inputs (phone: `^\+1\d{10}$`)
- **SQL Injection:** Use SQLAlchemy ORM exclusively
- **Privacy:** Mask phone numbers in logs (last 4 digits)
- **HTTPS:** Enforce in production via nginx reverse proxy

---

## Testing Requirements

**Current Coverage:**
- Overall: 85% (288 tests passing)
- Rotation algorithm: 100% (30 tests)
- Critical paths: 100% (SMS, scheduler)

**Target:** Maintain 80%+ coverage

**Test Structure:** Mirror `src/` directory in `tests/`

**Critical Test Cases:**
- Rotation algorithm (multiple weeks, team sizes, edge cases)
- Schedule regeneration on team changes
- SMS retry logic on failures
- Scheduler execution timing
- API validation (phone format, duplicates)

**Test Patterns:** `/docs/reference/code-patterns.md#test-fixtures`

---

## Common Patterns

### Repository Pattern
```python
# Extend BaseRepository for domain-specific queries
class TeamMemberRepository(BaseRepository[TeamMember]):
    def get_active(self) -> List[TeamMember]:
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).all()
```

### Service Layer
```python
# Coordinate between API and repositories
class TeamMemberService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TeamMemberRepository(db)
```

**Full Examples:** `/docs/reference/code-patterns.md`

---

## Important Constraints

1. **Timezone:** Always use America/Chicago (CST/CDT) via `pytz`
2. **Phone Format:** E.164 only (+1XXXXXXXXXX)
3. **Shift Config:** Default 6 shifts, Shift 2 is 48h double (Tue-Wed)
4. **Schedule Gen:** Minimum 4 weeks advance
5. **Transactions:** Explicit transactions with rollback on errors

---

## Common Pitfalls (Avoid These)

❌ Using system cron → ✅ Use APScheduler
❌ Hardcoding timezones → ✅ Use `timezone('America/Chicago')`
❌ Skipping phone validation → ✅ Validate E.164 format
❌ Missing indexes → ✅ Index frequently queried fields
❌ Regenerating entire schedule → ✅ Regenerate from change date forward
❌ Storing secrets in code → ✅ Use environment variables

---

## RPI Workflow (Research → Plan → Implement)

WhoseOnFirst uses a lightweight 3-phase process adapted from HexTrackr:

**Phase 1: RESEARCH** (30-90 min)
- Use MCP tools FIRST (memento, claude-context, sequential-thinking)
- Document current state with file:line references
- Identify impacted files and Docker rebuild points

**Phase 2: PLAN** (30-60 min)
- Break into 3-10 tasks (15-60 min each)
- Write before/after code snippets
- Mark one task as NEXT

**Phase 3: IMPLEMENT** (1-3 hours)
- Execute with Docker rebuild checkpoints
- Commit every 1-3 tasks
- Verify in logs before proceeding

**When to use:**
- Bug fixes and corrections
- Enhancements to existing features
- Small, well-defined features

**Full Process:** `/docs/RPI_PROCESS.md`

---

## MCP Tools & Knowledge Management

### Token Efficiency Hierarchy (use in order)

```javascript
// 1. Find historical decisions
memento__semantic_search({
  query: "docker workflow auto-renewal pattern",
  min_similarity: 0.6
})

// 2. Locate current code
claude-context__search_code({
  path: "/Volumes/DATA/GitHub/WhoseOnFirst",
  query: "schedule generation rotation algorithm",
  limit: 10
})

// 3. Break down complex problems
sequential-thinking__sequentialthinking({
  thought: "How does auto-renewal integrate with scheduler?",
  thoughtNumber: 1,
  totalThoughts: 5
})

// 4. Manual file operations - only after pinpointing exact files
```

**Critical:** Use semantic search FIRST. Saves 80-90% tokens.

### Slash Commands

- `/codebase-index` - Index for semantic search (after major changes)
- `/codebase-search [query]` - Natural language code search
- `/recall-conversation id:SESSION_ID` - Retrieve past session
- `/save-session [keyword]` - Save session + insights

**Session ID Format:** `WHOSEONFIRST-{KEYWORD}-{YYYYMMDD}-{HHMMSS}`

---

## Linear Integration

**Team:** WhoseOnFirst
**URL:** https://linear.app/hextrackr

**Issue Format:**
- Descriptive titles (e.g., "Schedule Auto-Renewal Feature")
- Types: Feature, Bug, Enhancement, Documentation
- Status: Todo → In Progress → Done
- Labels: backend, frontend, scheduler, docker, database, testing

**Recent Completed:**
- [WHO-2](https://linear.app/hextrackr/issue/WHO-2): Schedule Auto-Renewal ✅
- [WHO-3](https://linear.app/hextrackr/issue/WHO-3): Pagination Bug Fix ✅
- [WHO-4](https://linear.app/hextrackr/issue/WHO-4): Docker-First Workflow ✅

---

## Memento Knowledge Graph

**Entity Types:**
- `WHOSEONFIRST:DEVELOPMENT:SESSION`
- `WHOSEONFIRST:WORKFLOW:PATTERN`
- `WHOSEONFIRST:BACKEND:INSIGHT`
- `WHOSEONFIRST:SCHEDULER:DECISION`

**Required Tags:**
- `project:whoseonfirst` (always)
- `linear:WHO-X` (if related)
- Domain: `backend`, `frontend`, `scheduler`, `docker`
- Status: `completed`, `in-progress`
- Temporal: `week-XX-YYYY`, `vX.X.X`

**Taxonomy:** `/docs/TAXONOMY.md`

---

## Project Phases

**Phase 1: MVP** ✅ COMPLETE (v1.0.2)
- All backend features implemented
- All frontend pages with live data
- Docker containerization complete
- Authentication system implemented

**Phase 2: Deployment & Auth** 🔄 IN PLANNING
- Offline installer (air-gapped deployment)
- HTTPS support
- RHEL 10 production deployment
- Twilio 10DLC completion

**Phase 3: Enhancements** 📋 PLANNED
- Manual shift overrides (vacation/swap)
- Multi-level SMS (Primary/Secondary/Tertiary)
- Email backup notifications
- Auto-regeneration on config changes

**Phase 4: Advanced Features** 💭 FUTURE
- Multi-team support
- PostgreSQL migration
- Teams/Slack integration
- Mobile app (React Native/Flutter)

**Complete Roadmap:** Linear (Team: WhoseOnFirst) + `/docs/planning/PRD.md`

---

## When Creating New Code

1. ✅ Follow layered architecture (API → Service → Repository)
2. ✅ Use type hints everywhere (MyPy validation)
3. ✅ Write tests first (especially critical paths)
4. ✅ Handle timezones explicitly (America/Chicago)
5. ✅ Log important events with context
6. ✅ Document complex logic (rotation algorithm)
7. ✅ Validate all inputs (Pydantic models)
8. ✅ Use dependency injection (FastAPI `Depends()`)

---

## Additional Resources

- **PRD (Requirements):** `/docs/planning/PRD.md`
- **Architecture:** `/docs/planning/architecture.md`
- **Tech Stack:** `/docs/planning/technical-stack.md`
- **Code Patterns:** `/docs/reference/code-patterns.md`
- **RPI Process:** `/docs/RPI_PROCESS.md`
- **Taxonomy:** `/docs/TAXONOMY.md`
- **Documentation Guide:** `/docs/DOCUMENTATION_GUIDE.md`

---

**Last Updated:** 2025-11-10
**Version:** 1.0.2
**File Size:** ~10KB (lean and focused)
