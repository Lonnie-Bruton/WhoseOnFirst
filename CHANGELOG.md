# Changelog

All notable changes to the WhoseOnFirst project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Phase 1 Frontend Implementation** - Team Members UI (COMPLETE ✅)
  - Fully functional Team Members page with live API integration
  - SortableJS drag-and-drop for rotation order management
  - Real-time CRUD operations (Create, Read, Update, Activate/Deactivate, Permanent Delete)
  - **Permanent Delete** with Shift+Click - hold Shift and click Deactivate to trigger hard delete
    - Confirmation modal requires typing member's name exactly
    - Red warning header and alerts to prevent accidental deletion
    - New API endpoint: `DELETE /api/v1/team-members/{id}/permanent`
  - Active/Inactive filtering (simplified to two views)
  - Loading states and error handling
  - Auto-reload after mutations for clean state management
  - Bootstrap 5 modals for add/edit operations
  - E.164 phone number validation
  - Color-coded member cards (7 WCAG AA compliant colors)
  - Rotation numbers (1-based) displayed prominently with high contrast
  - Member initials in colored avatars
  - Responsive design with Tabler CSS framework
  - Light blue-gray page background for better card separation
  - Removed redundant Active/Inactive status badges (context makes it obvious)

- **Phase 2 Frontend Implementation** - Shift Configuration UI (COMPLETE ✅)
  - Fully functional Shift Configuration page with live API integration
  - Complete CRUD operations (Create, Read, Update, Delete)
  - **Smart Add Shift Modal** with enhanced UX:
    - Auto-populated shift number (finds next available 1-7)
    - Day selector with checkboxes instead of error-prone text input
    - Smart validation: 1 day for 24h shifts, 2 consecutive days for 48h shifts
    - Consecutive day validation (prevents non-adjacent selections for 48h shifts)
    - Dynamic hints that update based on duration selection
    - Field ordering optimized (Duration → Days → Start Time)
  - **Weekly Coverage Timeline** (visual coverage analysis):
    - 7 mini cards showing coverage status for each day of the week
    - Large checkmark/X icons for instant gap identification
    - Progress bar showing total coverage (0-168 hours)
    - Color-coded status badges (Full Coverage/Incomplete/Overlapping)
    - Warning alerts when coverage gaps exist (shows exact hours missing)
    - Duration badges matching main table styling (24h blue, 48h purple)
  - WCAG AA compliant color scheme for duration badges (high contrast text)
  - Shifts table with sortable columns and action buttons
  - Delete confirmation with cascade warning
  - Auto-reload after mutations for clean state management
  - Bootstrap 5 modals for add/edit operations
  - Empty state handling with helpful prompts
  - Example weekly pattern reference card
  - Responsive design with Tabler CSS framework
  - Light blue-gray page background consistent with Team Members page

- **Team Member Rotation Ordering** - Custom rotation order support (COMPLETE ✅)
  - Added `rotation_order` field to `team_members` table via Alembic migration
  - Updated `TeamMember` model with `rotation_order` integer field (nullable for flexibility)
  - Added `rotation_order` to `TeamMemberResponse` schema for API responses
  - New repository methods:
    - `TeamMemberRepository.get_max_rotation_order()` - Get highest rotation order value
    - `TeamMemberRepository.update_rotation_orders(order_mapping)` - Bulk update rotation positions
    - `TeamMemberRepository.get_ordered_for_rotation()` - Get members sorted by rotation_order
  - Updated `RotationAlgorithmService._get_team_members()` to sort by rotation_order (with ID fallback)
  - New API endpoint: `PUT /api/v1/team-members/reorder` for updating rotation positions
  - New Pydantic schema: `TeamMemberReorderRequest` with validation for order mappings
  - Service method: `TeamMemberService.update_rotation_orders()` with business logic
  - Preserves existing rotation behavior for members without rotation_order set
  - All 288 existing tests passing - no regressions

### Fixed
- **API Route Ordering** - Fixed `/reorder` endpoint routing conflict
  - Moved `/reorder` route before `/{member_id}` route in team_members router
  - FastAPI was incorrectly matching `/team-members/reorder` to `/{member_id}` route
  - This caused "Input should be a valid integer" errors when trying to save rotation order

### Changed
- **TEMPORARY: Phone Uniqueness Disabled for Testing**
  - Created migration `200f01c20965_temporarily_remove_phone_unique_constraint`
  - Removed unique constraint on `team_members.phone` field
  - Commented out duplicate phone validation in `TeamMemberService`
  - Allows multiple test users with same phone number for SMS rotation dry run testing
  - ⚠️ **TODO: Run `alembic downgrade -1` and re-enable validation before production!**
- **Frontend UI Mockups** - Complete Tabler-based admin dashboard (COMPLETE ✅)
  - `index.html` - Dashboard with calendar view, stats cards, and recent notifications
  - `team-members.html` - Team member management with CRUD operations
  - `shifts.html` - Shift configuration and assignment history
  - `schedule.html` - Schedule generation interface with algorithm selection
  - `notifications.html` - SMS notification history and Twilio configuration
  - Responsive design with Tabler CSS framework v1.0.0-beta20
  - Consistent custom SVG logo and navigation across all pages
  - Color-coded team members (7 distinct colors for visual identification)
  - Modal dialogs for data entry and editing
  - API integration stubs with comprehensive TODO comments for backend wiring
  - Fairness metrics and analytics displays
  - Template-based SMS message configuration
  - Comprehensive notification history with filtering and pagination
  - Algorithm selection UI (Round Robin, Weighted Fair, Preference-Based)
  - Schedule preview and generation settings
  - Twilio configuration status and testing interface
- **Twilio SMS Integration** - Production-ready SMS notification delivery (COMPLETE ✅)
  - `SMSService` - Complete Twilio integration with retry logic and error handling
  - Exponential backoff retry logic (3 attempts: 0s, 60s, 120s delay)
  - Smart error classification (retryable vs non-retryable Twilio errors)
  - Batch notification sending for multiple schedules
  - SMS message composition (under 160 characters for single SMS)
  - Phone number sanitization for logging (privacy)
  - Notification log integration for full audit trail
  - Delivery status checking via Twilio API
  - Mock mode for testing without Twilio credentials
  - Comprehensive error handling with custom exceptions
  - 27 comprehensive tests with 85% coverage (27/27 passing)
  - Integration with ScheduleManager for automated daily sending
- **APScheduler Integration** - Automated daily SMS notifications at 8:00 AM CST (COMPLETE ✅)
  - `ScheduleManager` class for managing BackgroundScheduler lifecycle
  - Daily notification job with CronTrigger at 8:00 AM America/Chicago
  - FastAPI lifespan integration for automatic start/stop
  - `send_daily_notifications()` function to process pending notifications
  - Manual trigger endpoint: POST /api/v1/schedules/notifications/trigger
  - Job status endpoint: GET /api/v1/schedules/notifications/status
  - Database session management for background jobs
  - Singleton pattern for global scheduler instance
  - Comprehensive logging for monitoring and debugging
  - Misfire grace time (5 minutes) for missed jobs
  - Coalesce setting to combine multiple missed runs
- **API Layer** - RESTful FastAPI endpoints with automatic OpenAPI documentation (COMPLETE ✅)
  - `src/main.py` - FastAPI application with CORS, routing, health checks
  - **Team Members API** (`/api/v1/team-members/`) - Full CRUD operations
    - GET / - List all members with optional active filter
    - GET /{id} - Get specific member
    - POST / - Create new member with phone validation
    - PUT /{id} - Update member details
    - DELETE /{id} - Soft delete (deactivate)
    - POST /{id}/activate - Reactivate member
  - **Shifts API** (`/api/v1/shifts/`) - Shift configuration management
    - GET / - List all shift configurations
    - GET /{id} - Get specific shift
    - POST / - Create new shift with validation
    - PUT /{id} - Update shift configuration
    - DELETE /{id} - Delete shift (cascades to schedules)
  - **Schedules API** (`/api/v1/schedules/`) - Schedule generation and queries
    - GET /current - Current week's schedule
    - GET /upcoming - Upcoming schedules (configurable weeks)
    - GET / - Query by date range
    - GET /member/{id} - Member-specific schedules
    - GET /member/{id}/next - Next assignment for member
    - POST /generate - Generate schedules (with force option)
    - POST /regenerate - Regenerate from date forward
  - **Pydantic Schemas** - Request/response validation
    - `TeamMemberCreate`, `TeamMemberUpdate`, `TeamMemberResponse`
    - `ShiftCreate`, `ShiftUpdate`, `ShiftResponse`
    - `ScheduleResponse`, `ScheduleGenerateRequest`, `ScheduleRegenerateRequest`
    - Phone validation (E.164 format)
    - Timezone validation (America/Chicago required)
    - Start time validation (HH:MM format)
    - Duration validation (24h or 48h)
  - **API Tests** - Comprehensive test coverage
    - 22 team member endpoint tests
    - 25+ shift endpoint tests
    - 25+ schedule endpoint tests
    - Integration tests for full workflows
    - TestClient with database session override
  - **Error Handling** - Consistent HTTP status codes
    - 200/201 for success
    - 400 for validation errors
    - 404 for not found
    - 422 for Pydantic validation failures
  - **OpenAPI Documentation** - Auto-generated API docs
    - Swagger UI available at `/docs`
    - ReDoc available at `/redoc`
    - Complete request/response examples
- **Schedule Service** - Orchestration layer for schedule generation and management (COMPLETE ✅)
  - `ScheduleService` - Coordinates between rotation algorithm and database persistence
  - Schedule generation with conflict prevention and force regeneration
  - Query methods: current week, upcoming schedules, date ranges, member-specific
  - Schedule regeneration when team composition changes
  - Notification tracking and management
  - Timezone-aware datetime validation (America/Chicago)
  - 28 comprehensive tests with 98% coverage (28/28 passing)
  - Integration with RotationAlgorithmService and ScheduleRepository
  - Custom exceptions: ScheduleAlreadyExistsError, InvalidDateRangeError
- **Rotation Algorithm Service** - Core circular rotation scheduler (COMPLETE ✅)
  - `RotationAlgorithmService` - Implements fair circular rotation for on-call assignments
  - Simple algorithm: team members rotate through shifts weekly (Shift N → Shift N+1)
  - Handles any team size (1 to 15+ members) with automatic position wrapping
  - Double-shift support (Tuesday-Wednesday 48h) naturally distributes workload
  - Timezone-aware datetime handling (America/Chicago)
  - Returns data compatible with ScheduleRepository.bulk_create()
  - 30 comprehensive tests with 100% coverage
  - Edge case handling: single member, large teams, more shifts than members, etc.
- **Service layer implementation** with comprehensive business logic
  - `TeamMemberService` - Team member management with phone validation and activation/deactivation
  - `ShiftService` - Shift configuration management with validation and weekend shift identification
  - Service-specific exceptions for granular error handling
  - Integration points for future schedule regeneration (Phase 2)
- Service layer test suite
  - 133 comprehensive tests for service layer (100% pass rate)
  - Tests for CRUD operations, validation, error handling, and business rules
  - Mock-free testing using real database sessions
  - Rotation algorithm tests: circular rotation, edge cases, datetime handling, integration
  - Schedule service tests: generation, queries, regeneration, notifications, integration
  - Repository timezone handling tests (naive/aware datetime conversion for SQLite)
- Repository layer implementation with full CRUD operations
  - `BaseRepository` - Generic repository with common database operations
  - `TeamMemberRepository` - Team member specific queries (phone validation, active/inactive)
  - `ShiftRepository` - Shift configuration management (weekend shifts, duration filters)
  - `ScheduleRepository` - Complex schedule queries (date ranges, notifications, bulk operations)
  - `NotificationLogRepository` - SMS delivery tracking and audit queries
- Repository layer test suite
  - 70 comprehensive tests for repository layer (100% pass rate)
  - Type-safe repository interfaces using Python generics
  - Comprehensive error handling with SQLAlchemy exception management
  - Query optimization with eager loading (joinedload) for relationships
  - Pagination support in BaseRepository get_all() method
  - Bulk insert operations for schedule generation efficiency

### Technical Details
- **Frontend:** 5 HTML files, ~2,500 lines of code
  - Tabler CSS v1.0.0-beta20 for UI components
  - Tabler Icons for consistent iconography
  - Vanilla JavaScript for API interactions (no framework dependencies)
  - Responsive design (mobile-first approach)
  - All pages ready for backend API integration
- **Scheduler:** APScheduler 3.10.4 with BackgroundScheduler
  - America/Chicago timezone configuration
  - Cron trigger: hour=8, minute=0 (daily at 8:00 AM CST)
  - Memory job store (can be upgraded to SQLAlchemyJobStore)
  - Max instances: 1 (prevent concurrent runs)
  - Next scheduled run: 2025-11-06 08:00:00-06:00
  - 305 lines of scheduler code with lifecycle management
- **Services:** 5 service files, 461 statements, 85-100% test coverage
  - `ScheduleService`: 57 statements, 98% covered ✅
  - `RotationAlgorithmService`: 63 statements, 100% covered ✅
  - `SMSService`: 146 statements, 85% covered ✅
  - `TeamMemberService`: 84 statements, 90% covered
  - `ShiftService`: 111 statements, 87% covered
  - Full business logic validation (phone format, shift numbers, durations, day names)
  - Proper exception hierarchy for error handling
  - Timezone-aware datetime handling (America/Chicago)
  - Production-ready Twilio integration with retry logic
- **Repositories:** 6 repository files, 1,447 lines of code
  - All repositories extend BaseRepository for consistency
  - Full type hints for IDE support and MyPy validation
  - Follows Repository Pattern from architecture.md
  - Uses SQLAlchemy ORM exclusively (no raw SQL)
- **Tests:** 288 total tests passing (58 API + 70 repository + 160 service)
  - Overall project coverage: 79% (target: 80%)
  - Service layer coverage: 85-100%
  - Repository layer coverage: 63-73%
  - API layer coverage: 79-96%
  - Rotation algorithm: 30 tests, 100% coverage ✅
  - Schedule service: 28 tests, 98% coverage ✅
  - SMS service: 27 tests, 85% coverage ✅
  - Repository timezone handling for SQLite (naive/aware datetime conversion)

---

## [0.1.0] - 2025-11-04

### Added
- Database layer implementation
  - SQLAlchemy configuration with SQLite support
  - Database session management with dependency injection
  - Base model with declarative_base
- Four core SQLAlchemy models:
  - `TeamMember` - Team member information with E.164 phone validation
  - `Shift` - Shift configuration (shift number, duration, day of week)
  - `Schedule` - Schedule assignments linking members to shifts
  - `NotificationLog` - SMS notification tracking and audit trail
- Alembic integration for database migrations
  - Initial migration with complete schema (4 tables, 20+ indexes)
  - Migration configuration supporting both SQLite and PostgreSQL
- Model utility methods:
  - `to_dict()` - Convert models to dictionaries for API responses
  - `validate_phone()` - E.164 phone number validation
  - `validate_status()` - Notification status validation
  - Property methods for checking schedule/notification states
- Database initialization utilities (`init_db()`, `drop_db()`)
- Relationship mappings with cascade delete

### Technical Details
- Total: 11 files created, 974 lines of code
- Database: SQLite with migration path to PostgreSQL
- ORM: SQLAlchemy 2.0.31+ with declarative models
- Migrations: Alembic 1.12.0+
- Full foreign key constraints with CASCADE delete
- Strategic indexing for query performance

---

## [0.0.1] - 2025-11-04

### Added
- Initial project setup and planning documentation
- Comprehensive Product Requirements Document (PRD.md)
  - 40+ functional requirements
  - 20+ non-functional requirements
  - Use cases and examples
  - Timeline and phases
  - Risk analysis
- Technology Research (research-notes.md)
  - Framework comparison (FastAPI vs Flask)
  - Scheduler research (APScheduler)
  - SMS integration (Twilio)
  - Database selection (SQLite vs PostgreSQL)
  - 25+ sources cited
- Technical Stack Documentation (technical-stack.md)
  - Complete technology stack with versions
  - Detailed rationale for each choice
  - Code examples and configuration templates
  - Security considerations
  - Migration paths
- System Architecture (architecture.md)
  - High-level architecture diagrams
  - Component architecture
  - API endpoint structure
  - Service layer design
  - Database schema (DDL)
  - Data flow diagrams
  - Deployment architecture
  - Security architecture
  - Architecture Decision Records (ADRs)
- Developer Documentation
  - README.md - Project overview and quick start
  - SETUP.md - Initial setup instructions
  - DEVELOPMENT.md - Developer workflow guide
  - CLAUDE.md - Claude Code guidance and patterns
- Project Infrastructure
  - Python virtual environment setup
  - requirements.txt and requirements-dev.txt
  - .env.example environment template
  - .gitignore with Python/IDE patterns
  - Project directory structure
- Git repository initialization
  - Initial commit to local repository
  - GitHub repository creation
  - Remote tracking configured

### Technical Details
- Total documentation: ~26,000+ words
- Python version: 3.11+
- Primary IDE: Claude Code CLI
- Project management: Claude Web with memory
- Version control: Git + GitHub

---

## Project Phases

### Phase 1: MVP (Weeks 1-6) - 🚧 In Progress
**Current Status:** ~90% Complete
- [x] Planning and documentation
- [x] Database models and migrations
- [x] Repository layer
- [x] Rotation algorithm (RotationAlgorithmService)
- [x] Schedule service (ScheduleService)
- [x] Team member service (TeamMemberService)
- [x] Shift service (ShiftService)
- [x] API endpoints (FastAPI routes)
- [x] APScheduler integration
- [x] Twilio SMS service
- [x] Admin dashboard UI mockups
- [ ] Backend-Frontend integration
- [ ] Docker containerization
- [x] Testing (79% coverage - target: 80%)

### Phase 2: Enhancement (Weeks 7-10) - 📋 Planned
- [ ] Multi-user authentication (JWT)
- [ ] Enhanced UI/UX
- [ ] Email notification backup
- [ ] Advanced reporting and analytics
- [ ] Performance optimization
- [ ] PostgreSQL migration

### Phase 3: Integration (Weeks 11-14) - 💭 Future
- [ ] Microsoft Teams integration
- [ ] REST API for external systems
- [ ] Calendar export (iCal format)
- [ ] Webhook support for events

### Phase 4: Scale (Weeks 15+) - 🔮 Vision
- [ ] Multi-team support
- [ ] Mobile application (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] High availability setup

---

## Development Standards

### Versioning
- **0.x.y** - Pre-release versions (Phase 1)
- **1.0.0** - First production release (Phase 1 MVP complete)
- **1.x.0** - Minor updates (new features)
- **1.x.y** - Patches (bug fixes)

### Commit Guidelines
- Use conventional commit format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Example: `feat(repository): add TeamMemberRepository with phone validation`

### Testing Requirements
- Minimum 80% code coverage
- 100% coverage for critical paths (rotation algorithm, SMS, scheduler)
- All tests must pass before merging to main
- Integration tests for API endpoints
- Unit tests for services and repositories

### Documentation Requirements
- Update CHANGELOG.md for all notable changes
- Document all public APIs with docstrings
- Update README.md when features change user-facing behavior
- Maintain architecture.md when design decisions change
- Add ADRs (Architecture Decision Records) for significant choices

---

## Links

- [Repository](https://github.com/Lonnie-Bruton/WhoseOnFirst)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/Lonnie-Bruton/WhoseOnFirst/issues)
- [PRD](docs/planning/PRD.md)
- [Architecture](docs/planning/architecture.md)

---

[Unreleased]: https://github.com/Lonnie-Bruton/WhoseOnFirst/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Lonnie-Bruton/WhoseOnFirst/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/Lonnie-Bruton/WhoseOnFirst/releases/tag/v0.0.1
