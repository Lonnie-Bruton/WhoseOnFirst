# Changelog

All notable changes to the WhoseOnFirst project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Repository layer implementation with full CRUD operations
  - `BaseRepository` - Generic repository with common database operations
  - `TeamMemberRepository` - Team member specific queries (phone validation, active/inactive)
  - `ShiftRepository` - Shift configuration management (weekend shifts, duration filters)
  - `ScheduleRepository` - Complex schedule queries (date ranges, notifications, bulk operations)
  - `NotificationLogRepository` - SMS delivery tracking and audit queries
- Type-safe repository interfaces using Python generics
- Comprehensive error handling with SQLAlchemy exception management
- Query optimization with eager loading (joinedload) for relationships
- Pagination support in BaseRepository get_all() method
- Bulk insert operations for schedule generation efficiency
- Repository layer exports via `__init__.py`

### Technical Details
- Total: 6 repository files, 1,447 lines of code
- All repositories extend BaseRepository for consistency
- Full type hints for IDE support and MyPy validation
- Follows Repository Pattern from architecture.md
- Uses SQLAlchemy ORM exclusively (no raw SQL)

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
**Current Status:** ~25% Complete
- [x] Planning and documentation
- [x] Database models and migrations
- [x] Repository layer
- [ ] Service layer
- [ ] API endpoints (FastAPI routes)
- [ ] Rotation algorithm
- [ ] APScheduler integration
- [ ] Twilio SMS service
- [ ] Admin dashboard (basic UI)
- [ ] Docker containerization
- [ ] Testing (>80% coverage)

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
