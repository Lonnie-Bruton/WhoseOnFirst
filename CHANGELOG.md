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

- **Phase 3 Frontend Implementation** - Schedule Generation UI (COMPLETE ✅)
  - Fully functional Schedule Generation page with live API integration
  - **Create Schedule Card** with smart defaults:
    - Auto-populated start date (next Monday)
    - Week duration selector (1, 2, 4, 8, 12 weeks)
    - Force regenerate option for overwriting existing schedules
    - Clear error messages when team members or shifts are missing
  - **Schedule Status Card** showing real-time stats:
    - Active team members count
    - Configured shifts count
    - Upcoming schedules count
    - Coverage period (X weeks)
    - Date range (start - end)
    - Visual progress indicator
  - **14-Day Preview Card** (full-width display):
    - Day-by-day mini cards showing rotation pattern
    - Each day shows assigned member, shift number, and duration badge
    - Color-coded member avatars matching team member colors
    - **48-hour shift fix**: Multi-day shifts now correctly display on ALL days they cover
    - Date range checking: `currentDate >= schedStart && currentDate < schedEnd`
    - Purple badges for 48h shifts, blue badges for 24h shifts
    - Visual "No coverage" indicators for gaps
    - Responsive grid layout (2-6 cards per row depending on screen size)
  - **View All Schedules Modal** with comprehensive table:
    - Full schedule listing with member names, shift details, date ranges
    - Duration badges color-coded by shift length
    - Scrollable modal for large datasets
    - Clean Tabler table styling
  - **Multi-source data integration**:
    - Combines data from `/api/v1/schedules/`, `/api/v1/team-members/`, and `/api/v1/shifts/`
    - Client-side data matching by IDs (team_member_id, shift_id)
    - Handles missing nested objects from API (only returns IDs, not full objects)
  - Auto-reload after schedule generation
  - Loading states and error handling
  - Bootstrap 5 modals and responsive design
  - Light blue-gray page background consistent with other pages

- **Phase 4 Frontend Implementation** - Notifications UI (COMPLETE ✅)
  - Simplified MVP version focused on essential features
  - **API Endpoints** (New):
    - `GET /api/v1/notifications/recent?limit=50` - Fetch recent notification logs
    - `GET /api/v1/notifications/stats?days=30` - Get statistics and delivery rates
    - `GET /api/v1/notifications/failed?hours=24` - Get failed notifications
    - `GET /api/v1/notifications/{id}` - Get specific notification by ID
  - **Notification Stats Cards** with real-time data:
    - Total Sent (all-time count from notification_log table)
    - This Month (current month count)
    - Delivery Rate (calculated success percentage with color-coded labels)
    - Failed Count (requires attention indicator)
  - **Notification History Table**:
    - Recent 50 notifications from database
    - Team member color-coded avatars
    - Masked phone numbers (last 4 digits)
    - Status badges (success, failed, pending)
    - Truncated Twilio SIDs
    - Refresh button for manual reload
  - **Read-Only SMS Template Display**:
    - Current template with send time (8:00 AM CST)
    - Template variables documented
    - Active status indicator
  - **Send Test SMS Button**:
    - Uses existing `/api/v1/schedules/notifications/trigger` endpoint
    - Auto-refreshes stats and history after send
    - Confirmation dialog before sending
  - **Removed for MVP** (keeping it simple):
    - Notification Schedule toggles (reminder notifications, weekly summary)
    - SMS Template editing UI (use environment variables for MVP)
    - Twilio Configuration UI (use .env file for MVP)
  - **Multi-source data fetching**:
    - Combines notifications, schedules, and team members APIs
    - Client-side matching to show recipient names and colors
  - Consistent design with other pages (Tabler CSS, team colors, responsive)

- **Dashboard UI Upgrade** - Live data integration (COMPLETE ✅)
  - Removed "Generate Schedule" and "Send Test SMS" buttons (use dedicated pages instead)
  - Removed SMS notification history table (moved to Notifications page)
  - Removed SMS stats cards (moved to Notifications page)
  - **Live Stats Cards**:
    - Active Team Members count (fetched from API)
    - **On-Call Escalation Chain** (wide card showing 3-tier backup):
      - Primary: Current on-call (or next if none active) with phone and time info
      - Secondary: Previous shift person (automatic backup)
      - Tertiary: 2 shifts ago (escalation contact)
      - Shows "Until" time for active, "Starts" time for future, "Ended" for past
      - Color-coded avatars matching team member colors
      - Full phone numbers displayed for quick contact
  - **Dynamic Calendar**:
    - Auto-generated from real schedule data via `/api/v1/schedules/upcoming`
    - Shows current month only (not hardcoded)
    - Weekend highlighting (light gray background)
    - Empty cells for days outside current month
    - 48-hour shift indicators with "(48h)" label
    - Color-coded badges matching team member colors
    - First names only for cleaner display
    - **Phone number on hover** - Tooltip shows full name and phone number
    - Pointer cursor on badges for better UX
  - **Dynamic Team Legend**:
    - Auto-generated from active team members
    - Color boxes matching calendar badges
    - Sorted by member ID for consistency
  - **Multi-source data fetching**:
    - Combines `/api/v1/team-members/`, `/api/v1/schedules/upcoming?weeks=8`, and `/api/v1/shifts/`
    - Parallel fetching for better performance
    - Client-side matching by IDs (team_member_id, shift_id)
  - **Focused design**: Calendar-centric view for quick on-call status overview

- **UI Polish & Standardization** - Visual consistency improvements (COMPLETE ✅)
  - **Dashboard Escalation Chain Enhancements**:
    - Added user initials to avatar circles (e.g., "LB", "BB", "GK")
    - Fixed escalation calculation to use rotation_order instead of schedule time
    - Secondary/Tertiary now based on rotation position (previous in rotation, not time)
    - Fixed bug where all avatars showed same color (now uses individual team colors)
    - Enhanced card depth with better shadows and borders
    - Light gray page background (#f1f5f9) for better card separation
  - **Centralized Color System** (16 unique WCAG AA compliant colors):
    - Expanded from 7 to 16 colors to eliminate duplicates (8+ team members had collisions)
    - Standardized all hex values across all 4 frontend pages
    - Updated all modulo operations from % 7 to % 16
    - Colors: Blue, Red, Green, Amber, Purple, Cyan, Orange, Pink, Teal, Yellow, Deep Purple, Dark Red, Navy, Forest Green, Rust, Violet
    - Same person always has same color everywhere (dashboard, calendar, team list, notifications)
    - All colors pass 4.5:1 contrast ratio on white backgrounds
  - **SMS Template Editor** (Notifications Page):
    - Full edit functionality with save/cancel/reset buttons
    - Real-time character counter (0-160+ characters)
    - SMS count calculator (multiples of 160 chars per SMS)
    - Template validation (no empty templates, warning if no variables)
    - LocalStorage persistence for MVP (can migrate to backend later)
    - Available variables: {name}, {start_time}, {end_time}, {duration}
    - Default template: "WhoseOnFirst Alert..." with shift details
  - **Consistent Card Styling** across all pages:
    - White cards with subtle shadows (0 1px 3px rgba(0,0,0,0.1))
    - Enhanced hover shadows (0 4px 12px rgba(0,0,0,0.15))
    - Light borders (#e2e8f0) for better definition
    - Smooth transitions (all 0.2s)
  - **Pages Updated**: index.html, team-members.html, schedule.html, notifications.html

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

### Known Limitations (MVP)
These are intentional scope limitations for the initial MVP release. Future enhancements are planned.

- **Manual Schedule Regeneration Required**
  - **Current Behavior**: Adding/removing team members or modifying shifts does NOT auto-regenerate schedule
  - **Workaround**: Admin must manually navigate to Schedule Generation page and click "Generate Schedule" with force=true
  - **Future Enhancement** (REQ-039): Auto-regeneration with warning banners
  - **Rationale**: Keeps MVP simple; explicit control prevents accidental overwrites

- **Single SMS Notification (Primary Only)**
  - **Current Behavior**: Only the primary on-call person receives SMS at 8:00 AM CST
  - **Workaround**: None needed - backup contacts visible on dashboard escalation chain
  - **Future Enhancement** (REQ-038): Send 3 SMS messages (Primary, Secondary, Tertiary) with escalation info
  - **Rationale**: Dashboard already calculates escalation chain; backend expansion is straightforward

- **No Manual Shift Overrides**
  - **Current Behavior**: Cannot manually assign a team member to a single shift occurrence
  - **Workaround**: Regenerate entire schedule or manually edit database (not recommended)
  - **Future Enhancement** (REQ-037): UI to select date/shift and apply one-time override
  - **Rationale**: Rotation algorithm is solid; override mechanism can be added without disrupting core logic

- **SMS Template Editing (LocalStorage Only)**
  - **Current Behavior**: Template changes stored in browser LocalStorage, not centralized
  - **Workaround**: Each admin must set template in their browser
  - **Future Enhancement**: Backend API endpoint for global template management
  - **Rationale**: LocalStorage works for single-admin MVP; easy to migrate later

### Fixed
- **Rotation Algorithm - Complete Rewrite** - Fixed to cycle through ALL team members (CRITICAL FIX)
  - **Bug**: With 8 members and 6 shifts, Lance B (member 7) never appeared in schedule
  - **Root Cause**: Formula used week number as offset instead of total shifts elapsed
    - Old: `week_offset = week % len(members)` → only rotated by 1 position per week
    - After 6 shifts in week 0, rotation should advance by 6, not 1
  - **New Formula**: `shifts_elapsed = (week * len(shifts)) + shift_index`
    - `member_index = shifts_elapsed % len(members)`
    - Continuously cycles through all members regardless of team size vs. shifts
  - **Now Works For**:
    - 1 member: Same person all shifts ✓
    - 2 members: Perfect alternation (A,B,A,B...) ✓
    - 8 members, 6 shifts: All 8 members cycle through (Lance B appears!) ✓
    - Any team size, any shift count: Fair continuous rotation ✓
  - **Dynamic Shift Configuration**: Automatically adjusts when shifts added/removed
    - Change from 6 to 7 shifts → formula uses new `len(shifts) = 7` ✓
  - All rotation tests updated and passing

- **Rotation Algorithm Direction** - Fixed rotation to move forward through shifts (PREVIOUS FIX)
  - Changed formula from `(shift_index + week_offset)` to `(shift_index - week_offset)`
  - Old behavior: Person moved BACKWARD through shifts each week (Shift 2 → Shift 1)
  - New behavior: Person moves FORWARD through shifts each week (Shift 2 → Shift 3)
  - Now correctly implements: "Each week, person on Shift N moves to Shift N+1"

- **Auto-Assign Rotation Order on Member Creation** - New members now get rotation numbers automatically
  - Added auto-assignment logic in `TeamMemberService.create()` method
  - New members get `rotation_order = max_existing_order + 1` automatically
  - Only applies to active members (inactive members have `rotation_order = null`)
  - Matches existing `activate()` method behavior for consistency
  - Fixes bug where manually added members (like Lance B) didn't show rotation number

- **API Route Ordering** - Fixed `/reorder` endpoint routing conflict
  - Moved `/reorder` route before `/{member_id}` route in team_members router
  - FastAPI was incorrectly matching `/team-members/reorder` to `/{member_id}` route
  - This caused "Input should be a valid integer" errors when trying to save rotation order

- **Schedule Preview Not Showing Upcoming Schedules** - Fixed date range filtering issue
  - Fixed `get_upcoming_weeks()` in `schedule_repository.py` to normalize start date to midnight
  - Previous behavior: Used `datetime.now()` which excluded schedules starting at 8:00 AM if checked after 8 AM
  - New behavior: Normalizes to start of day with `.replace(hour=0, minute=0, second=0, microsecond=0)`
  - This ensures all schedules starting today are included in the query
  - Fixed API validation limit in `/api/v1/schedules/upcoming` from 52 to 104 weeks
  - Allows frontend to fetch up to 2 years of schedules for preview and status cards
  - Resolves issue where status card showed wrong week count and preview showed no schedules

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
