# WhoseOnFirst - On-Call Team SMS Notifier

> Automated on-call rotation and SMS notification system for technical teams

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP%20complete-success.svg)](docs/MVP_STATUS.md)
[![Progress](https://img.shields.io/badge/progress-100%25-brightgreen.svg)](CHANGELOG.md)

---

## 🎯 Overview

WhoseOnFirst is an automated scheduling and notification system that manages fair on-call rotations for technical teams. The system ensures equitable shift distribution using simple circular rotation, schedules the 48-hour double shift during the workweek (Tue-Wed) to minimize weekend impact, and automatically notifies on-call personnel via SMS at the start of each shift.

### Key Features

- 📅 **Simple Circular Rotation** - Fair, predictable rotation where all team members cycle through continuously
- 📱 **Automated SMS Notifications** - Daily 8:00 AM CST notifications via Twilio
- ⚙️ **Flexible Shift Patterns** - Support for 24-hour and 48-hour shifts
- 🎨 **Polished Web Interface** - 4 fully functional pages with live data integration
- 🔄 **Dynamic Team Management** - Drag-and-drop rotation ordering, works with any team size
- 🐳 **Docker Ready** - Containerized for easy deployment on RHEL 10

---

## 📋 Project Status

**Current Phase:** MVP Complete ✅ - Ready for Docker Deployment
**Version:** 0.2.0
**Next Step:** Docker containerization and 1-week production trial
**Twilio Status:** ⏳ Awaiting 10DLC verification (messages hitting dashboard successfully)

### What's Complete

✅ **Backend (100%)**
- All 25 MVP requirements implemented
- 288 tests passing, rotation algorithm 100% coverage
- FastAPI REST API with 25+ endpoints
- APScheduler for daily SMS notifications
- Twilio integration verified (messages reaching dashboard)

✅ **Frontend (100%)**
- Dashboard with live data, escalation chain, dynamic calendar
- Team Members page with drag-and-drop ordering
- Shift Configuration with visual coverage timeline
- Schedule Generation with 2-week preview
- Notifications page with SMS template editing

✅ **Documentation (100%)**
- [MVP Status Report](docs/MVP_STATUS.md) - Comprehensive status and validation
- [Product Requirements](docs/planning/PRD.md) - All requirements met
- [Architecture](docs/planning/architecture.md) - System design validated
- [CHANGELOG](CHANGELOG.md) - Complete change history

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI 0.115+ | REST API framework with auto-documentation |
| **Server** | Uvicorn | High-performance ASGI server |
| **Scheduler** | APScheduler 3.10+ | Cron-based job scheduling (8:00 AM CST daily) |
| **Database** | SQLite → PostgreSQL | Embedded DB (MVP) → Enterprise DB (Phase 2+) |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction with Alembic migrations |
| **SMS** | Twilio Python SDK | SMS delivery service |
| **Frontend** | Vanilla JS + Bootstrap 5 + Tabler CSS | Responsive web interface |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker Desktop (for containerization)
- Twilio account with verified phone number
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/Lonnie-Bruton/WhoseOnFirst.git
cd WhoseOnFirst

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Twilio credentials:
#   TWILIO_ACCOUNT_SID=your_account_sid
#   TWILIO_AUTH_TOKEN=your_auth_token
#   TWILIO_FROM_NUMBER=+1XXXXXXXXXX

# Initialize database
alembic upgrade head

# Run backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &

# Run frontend server (separate terminal)
cd frontend
python3 -m http.server 8080

# Access application
# Frontend: http://localhost:8080
# API Docs: http://localhost:8000/docs
```

### Docker Deployment (Ready for Build)

```bash
# Build image
docker build -t whoseonfirst:0.2.0 .

# Run with docker-compose
docker-compose up -d

# View logs
docker logs -f whoseonfirst
```

---

## 📖 Usage

### Web Interface

Access at `http://localhost:8080` (or port configured in docker-compose)

**Available Pages:**
1. **Dashboard** - Current on-call status, escalation chain, monthly calendar
2. **Team Members** - Add/edit/reorder team members, drag-and-drop rotation order
3. **Shift Configuration** - Configure 24h/48h shifts, visual coverage timeline
4. **Schedule Generation** - Generate 4-104 weeks of rotation, 2-week preview
5. **Notifications** - SMS history, delivery stats, editable message template

### API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example API Calls

```bash
# Get current on-call schedule
curl http://localhost:8000/api/v1/schedules/current

# Add team member
curl -X POST http://localhost:8000/api/v1/team-members/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "+15551234567", "is_active": true}'

# Generate schedule for 4 weeks
curl -X POST 'http://localhost:8000/api/v1/schedules/generate?start_date=2025-11-10&weeks=4&force=true'

# Trigger test SMS notification
curl -X POST http://localhost:8000/api/v1/schedules/notifications/trigger
```

---

## 🗓️ Development Roadmap

### ✅ Phase 1: MVP (Complete - November 2025)
- [x] Requirements gathering and PRD
- [x] Technology research and stack selection
- [x] Architecture design and database schema
- [x] Repository layer (5 repositories, 70 tests)
- [x] Service layer (5 services, 160 tests)
- [x] API endpoints (25+ endpoints, 58 tests)
- [x] Rotation algorithm (30 tests, 100% coverage)
- [x] Twilio SMS integration (verified working)
- [x] APScheduler integration (8:00 AM CST daily)
- [x] Complete web interface (4 pages, live data)
- [x] Docker containerization setup

### 🔄 Phase 2: Production Validation (Next - 1-2 weeks)
- [ ] Docker deployment to RHEL 10 VM
- [ ] 1-week production trial with real SMS
- [ ] Twilio 10DLC verification completion
- [ ] Monitor notification delivery and logs
- [ ] Gather user feedback

### 📋 Phase 3: Enhancements (Planned - 2-4 weeks)
- [ ] Manual shift overrides (one-time exceptions)
- [ ] Multi-level SMS (Primary/Secondary/Tertiary notifications)
- [ ] Auto-regeneration on configuration changes
- [ ] Email notification backup
- [ ] Enhanced reporting and analytics

### 💭 Phase 4: Advanced Features (Future - 3+ months)
- [ ] Multi-team support
- [ ] PostgreSQL migration
- [ ] Microsoft Teams/Slack integration
- [ ] Mobile application
- [ ] REST API for external integrations

---

## 🏗️ Project Structure

```
WhoseOnFirst/
├── docs/                      # Documentation
│   ├── planning/             # Planning documents (PRD, architecture)
│   ├── MVP_STATUS.md         # Current project status
│   ├── DEVELOPMENT.md        # Development guide
│   └── SETUP.md              # Setup instructions
├── src/                      # Backend source code
│   ├── main.py              # FastAPI application entry
│   ├── api/                 # API routes (team-members, shifts, schedules, notifications)
│   ├── services/            # Business logic (5 services)
│   ├── models/              # SQLAlchemy models (4 tables)
│   ├── repositories/        # Data access layer (5 repositories)
│   ├── api/schemas/         # Pydantic schemas for validation
│   └── scheduler.py         # APScheduler configuration
├── frontend/                 # Web interface (4 pages)
│   ├── index.html           # Dashboard
│   ├── team-members.html    # Team management
│   ├── shifts.html          # Shift configuration
│   ├── schedule.html        # Schedule generation
│   └── notifications.html   # Notification history & templates
├── tests/                    # Test suite (288 tests)
├── alembic/                  # Database migrations
├── data/                     # SQLite database (gitignored)
├── .env.example             # Environment variables template
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run rotation algorithm tests (critical)
pytest tests/test_rotation_algorithm.py -v

# Run with verbose output
pytest -v --tb=short
```

**Test Coverage:**
- Rotation Algorithm: 100% (30 tests)
- Repository Layer: 85%+ (70 tests)
- Service Layer: 85-100% (160 tests)
- API Endpoints: 79-96% (58 tests)
- **Overall**: 79% (target: 80%+)

---

## 🔒 Security

### Credential Management
- All secrets in `.env` file (never committed)
- Twilio credentials as environment variables
- Database files have restricted permissions
- `.gitignore` configured for sensitive files

### Best Practices
- Input validation via Pydantic models
- SQL injection prevention (SQLAlchemy ORM only)
- Phone numbers sanitized in logs (E.164 format)
- HTTPS enforced in production (nginx reverse proxy)
- WCAG AA color contrast for accessibility

### SMS Consent
- SMS template includes opt-out instructions
- Consent policy documented in repository
- Phone numbers validated before storage

---

## 🤝 Contributing

This is currently a private internal project.

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with tests: `pytest tests/`
3. Update CHANGELOG.md
4. Commit: `git commit -m "feat: add feature"`
5. Push: `git push origin feature/your-feature`
6. Create pull request

### Code Standards
- Follow PEP 8 style guide
- Use type hints for all functions
- Maintain >80% test coverage
- Update documentation for API changes
- Write tests before code (TDD preferred)

---

## 📝 License

[License TBD - To be determined]

---

## 🙏 Acknowledgments

- **Twilio** - SMS delivery platform
- **FastAPI** - Modern, fast web framework
- **APScheduler** - Reliable job scheduling
- **SQLAlchemy** - Excellent ORM
- **Tabler** - Beautiful UI components
- **Claude (Anthropic)** - AI-assisted development

---

## 📞 Support

### Documentation
- [MVP Status Report](docs/MVP_STATUS.md) - Complete project overview
- [API Reference](http://localhost:8000/docs) - Interactive API docs
- [Architecture Guide](docs/planning/architecture.md) - System design
- [Development Guide](docs/DEVELOPMENT.md) - Dev workflow

### Known Limitations (MVP)
1. **Manual Schedule Regeneration** - Changes to team/shifts require manual regenerate (auto-regen planned for Phase 3)
2. **Single SMS Notification** - Only primary on-call notified (multi-level planned for Phase 3)
3. **No Shift Overrides** - Cannot manually override single shifts (planned for Phase 3)
4. **LocalStorage SMS Template** - Template stored per-browser (backend migration planned)

See [MVP_STATUS.md](docs/MVP_STATUS.md) for complete limitations and workarounds.

---

## 🔄 Change Log

See [CHANGELOG.md](CHANGELOG.md) for complete release history.

### Version 0.2.0 (2025-11-08) - MVP Complete ✅
- ✅ Complete frontend implementation (4 pages, live data)
- ✅ Rotation algorithm fix (all team members cycle through)
- ✅ 16-color system for visual clarity (WCAG AA compliant)
- ✅ Editable SMS templates with character counter
- ✅ On-call escalation chain display
- ✅ Drag-and-drop rotation ordering
- ✅ Comprehensive documentation (MVP_STATUS.md)
- ✅ Ready for Docker deployment

### Version 0.1.0 (2025-11-06) - Backend Complete ✅
- Complete backend with 288 passing tests
- Twilio SMS integration with retry logic
- APScheduler daily notifications (8:00 AM CST)
- Complete API layer with OpenAPI docs
- Service and repository layers implemented

---

## 📊 Project Metrics

- **Total Tests:** 288 (all passing ✅)
- **Test Coverage:** 79% (target: 80%+)
- **API Endpoints:** 25+ endpoints
- **Frontend Pages:** 4 complete pages
- **Documentation:** 35,000+ words
- **Team Size Support:** 1-16+ members (tested with 8)
- **Shift Flexibility:** Any number of 24h/48h shifts
- **Lines of Code:** ~12,000+ (backend + frontend)

---

**Built with ❤️ by Lonnie Bruton**

*Last Updated: November 8, 2025*
