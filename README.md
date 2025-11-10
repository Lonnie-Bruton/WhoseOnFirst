# WhoseOnFirst - On-Call Team SMS Notifier

> Automated on-call rotation and SMS notification system for technical teams

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-success.svg)](https://github.com/Lonnie-Bruton/WhoseOnFirst/releases/tag/v1.0.0)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](CHANGELOG.md)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b37c9c41b9644a9990be09eeda5bf014)](https://app.codacy.com/gh/Lonnie-Bruton/WhoseOnFirst/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

---

## 🎯 Overview

WhoseOnFirst is a production-ready on-call rotation and SMS notification system that manages fair shift assignments for technical teams. The system ensures equitable shift distribution using simple circular rotation, schedules the 48-hour double shift during the workweek (Tue-Wed) to minimize weekend impact, and automatically notifies on-call personnel via SMS at the start of each shift.

### Key Features

- 🔐 **Secure Authentication** - Role-based access control (Admin/Viewer) with Argon2id password hashing
- 📅 **Simple Circular Rotation** - Fair, predictable rotation where all team members cycle through continuously
- 📱 **Automated SMS Notifications** - Daily 8:00 AM CST notifications via Twilio
- ⚙️ **Flexible Shift Patterns** - Support for 24-hour and 48-hour shifts with visual coverage timeline
- 🎨 **Polished Web Interface** - 8 fully functional pages with live data integration
- 🔄 **Dynamic Team Management** - Drag-and-drop rotation ordering, works with any team size
- 📚 **Comprehensive Help System** - Built-in Twilio setup guide and troubleshooting
- 🐳 **Docker Ready** - Containerized for easy deployment

---

## 📋 Project Status

**Current Version:** 1.0.0 🎉
**Status:** Production Ready - MVP Complete
**Release Date:** November 9, 2025
**Next Phase:** Docker containerization for air-gapped RHEL deployment

### What's Complete

✅ **Backend (100%)**
- All 25 MVP requirements implemented
- 288 tests passing, 85% overall coverage
- FastAPI REST API with 30+ endpoints
- APScheduler for daily SMS notifications at 8:00 AM CST
- Twilio integration with retry logic and error handling
- Argon2id password hashing (OWASP 2025 compliant)

✅ **Frontend (100%)**
- Dashboard with live data, escalation chain, dynamic calendar
- Team Members page with drag-and-drop ordering
- Shift Configuration with visual coverage timeline
- Schedule Generation with 14-day preview
- Notifications page with SMS history and editable templates
- Help & Setup page with comprehensive Twilio guide
- Change Password page for all users
- Login page with branded design and easter egg

✅ **Authentication & Security (100%)**
- Session-based auth with HTTPOnly cookies
- Two-tier role system (Admin/Viewer)
- Protected routes with automatic redirect
- Password strength requirements
- Admin-only viewer password reset

✅ **Documentation (100%)**
- [CHANGELOG](CHANGELOG.md) - Complete v1.0.0 release notes
- [Product Requirements](docs/planning/PRD.md) - All requirements met
- [Architecture](docs/planning/architecture.md) - System design validated
- Built-in Help page with Twilio setup guide

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI 0.115+ | REST API framework with auto-documentation |
| **Server** | Uvicorn | High-performance ASGI server |
| **Scheduler** | APScheduler 3.10+ | Cron-based job scheduling (8:00 AM CST daily) |
| **Database** | SQLite → PostgreSQL | Embedded DB (MVP) → Enterprise DB (Phase 2+) |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction with Alembic migrations |
| **SMS** | Twilio Python SDK | SMS delivery service with retry logic |
| **Auth** | Argon2-CFFI | Password hashing (OWASP 2025 recommended) |
| **Frontend** | Vanilla JS + Tabler CSS | Responsive web interface (no build step) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Twilio account with verified phone number (see Help page for setup)
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
# Edit .env with your Twilio credentials (see Help page for guide)

# Initialize database
alembic upgrade head

# Run server (frontend served from FastAPI on port 8000)
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Access application
# Dashboard: http://localhost:8000/
# Login: admin/admin (change password immediately!)
# Help & Setup: http://localhost:8000/help.html
# API Docs: http://localhost:8000/docs
```

### Docker Deployment

#### Using Docker

```bash
# Build image
docker build -t whoseonfirst:1.0.0 .

# Run container
docker run -d --name whoseonfirst \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  whoseonfirst:1.0.0

# View logs
docker logs -f whoseonfirst

# Stop container
docker stop whoseonfirst

# Remove container
docker rm whoseonfirst
```

#### Using Docker Compose (Recommended)

```bash
# Start application (builds image if needed)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

#### Using Podman (RHEL/CentOS)

```bash
# Build image
podman build -t whoseonfirst:1.0.0 .

# Run container
podman run -d --name whoseonfirst \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data:Z \
  --env-file .env \
  whoseonfirst:1.0.0

# View logs
podman logs -f whoseonfirst

# Stop and remove
podman stop whoseonfirst
podman rm whoseonfirst
```

**Note:** The `:Z` flag on the volume mount is required for SELinux systems (RHEL/CentOS) to allow the container to write to the mounted directory.

#### Docker Troubleshooting

**TLS Certificate Errors:**
If you encounter TLS certificate errors when pulling images, this typically indicates a proxy or network configuration issue:
```
ERROR: tls: failed to verify certificate
```
Solutions:
- Configure Docker to use your corporate proxy settings
- Add necessary CA certificates to Docker's trust store
- Use an offline base image if deploying to air-gapped environments

**SELinux Permission Denied:**
If you see permission errors on RHEL/CentOS, ensure you use the `:Z` flag on volume mounts:
```bash
-v $(pwd)/data:/app/data:Z  # Note the :Z flag
```

**Port Already in Use:**
If port 8000 is already in use, you can map to a different port:
```bash
docker run -p 8080:8000 ...  # Maps host port 8080 to container port 8000
```

---

## 📖 Usage

### Web Interface

Access at `http://localhost:8000/` and login with default credentials:
- **Admin**: username=`admin`, password=`admin` (full access)
- **Viewer**: username=`viewer`, password=`viewer` (read-only)

⚠️ **IMPORTANT:** Change the admin password immediately after first login!

**Available Pages:**
1. **Dashboard** - Current on-call status, escalation chain, monthly calendar with phone numbers
2. **Team Members** - Add/edit/reorder team members, drag-and-drop rotation order (Admin only)
3. **Shift Configuration** - Configure 24h/48h shifts, visual coverage timeline (Admin only)
4. **Schedule Generation** - Generate 1-104 weeks of rotation, 14-day preview (Admin only)
5. **Notifications** - SMS history, delivery stats, editable message template (Admin only)
6. **Help & Setup** - Comprehensive Twilio configuration guide with troubleshooting (All users)
7. **Change Password** - Password management for all users
8. **Login** - Secure authentication with branded design

### API Documentation

Interactive API documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

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
- [x] Repository layer (6 repositories, 70 tests)
- [x] Service layer (5 services, 160 tests)
- [x] API endpoints (30+ endpoints, 58 tests)
- [x] Rotation algorithm (30 tests, 100% coverage)
- [x] Twilio SMS integration (verified working)
- [x] APScheduler integration (8:00 AM CST daily)
- [x] Authentication system (Argon2id, role-based access)
- [x] Complete web interface (8 pages, live data)
- [x] Help & Setup page with Twilio guide
- [x] **v1.0.0 RELEASE** 🎉

### 🚧 Phase 2: Deployment & Enhancement (In Progress)
- [x] Docker/Podman containerization
- [ ] Offline installer for air-gapped RHEL 10
- [ ] Production deployment validation
- [ ] Twilio 10DLC verification completion
- [ ] Settings UI for Twilio credentials (vs .env)
- [ ] Global SMS template management (vs LocalStorage)

### 📋 Phase 3: Advanced Features (Planned - 2-4 weeks)
- [ ] Manual shift overrides (one-time exceptions)
- [ ] Multi-level SMS (Primary/Secondary/Tertiary notifications)
- [ ] Auto-regeneration on configuration changes
- [ ] Email notification backup
- [ ] Enhanced reporting and analytics
- [ ] PTO/Vacation management

### 💭 Phase 4: Enterprise Features (Future - 3+ months)
- [ ] Multi-team support
- [ ] PostgreSQL migration
- [ ] Microsoft Teams/Slack integration
- [ ] Mobile application (iOS/Android)
- [ ] High availability setup
- [ ] Advanced analytics dashboard

---

## 🏗️ Project Structure

```
WhoseOnFirst/
├── docs/                      # Documentation
│   ├── planning/             # Planning documents (PRD, architecture)
│   └── DEVELOPMENT.md        # Development guide
├── src/                      # Backend source code
│   ├── main.py              # FastAPI application entry (v1.0.0)
│   ├── api/                 # API routes (auth, team-members, shifts, schedules, notifications)
│   ├── auth/                # Authentication utilities (Argon2id, sessions)
│   ├── services/            # Business logic (6 services)
│   ├── models/              # SQLAlchemy models (5 tables)
│   ├── repositories/        # Data access layer (6 repositories)
│   ├── api/schemas/         # Pydantic schemas for validation
│   └── scheduler/           # APScheduler configuration
├── frontend/                 # Web interface (8 pages)
│   ├── login.html           # Login page
│   ├── index.html           # Dashboard
│   ├── team-members.html    # Team management (Admin only)
│   ├── shifts.html          # Shift configuration (Admin only)
│   ├── schedule.html        # Schedule generation (Admin only)
│   ├── notifications.html   # Notification history (Admin only)
│   ├── help.html            # Help & Setup guide
│   └── change-password.html # Password management
├── tests/                    # Test suite (288 tests, 85% coverage)
├── alembic/                  # Database migrations
├── data/                     # SQLite database (gitignored)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── CHANGELOG.md            # Complete version history
└── README.md              # This file
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run critical rotation algorithm tests
pytest tests/test_rotation_algorithm.py -v

# Run auth tests
pytest tests/test_auth.py -v

# Run with verbose output
pytest -v --tb=short
```

**Test Coverage (v1.0.0):**
- **Overall**: 85% (288 tests, all passing ✅)
- Rotation Algorithm: 100% (30 tests)
- Repository Layer: 85%+ (70 tests)
- Service Layer: 85-100% (160 tests)
- API Endpoints: 79-96% (58 tests)

---

## 🔒 Security

### Authentication
- **Password Hashing**: Argon2id with OWASP 2025 parameters
- **Session Management**: HTTPOnly cookies with SameSite=Lax protection
- **Role-Based Access**: Two-tier system (Admin/Viewer)
- **Password Requirements**: Enforced strength for admin accounts

### Credential Management
- All secrets in `.env` file (never committed to Git)
- Twilio credentials as environment variables
- Database files have restricted permissions
- `.gitignore` configured for sensitive files

### Best Practices
- Input validation via Pydantic models
- SQL injection prevention (SQLAlchemy ORM only)
- Phone numbers sanitized in logs (masked last 4 digits)
- HTTPS enforced in production (nginx reverse proxy)
- WCAG AA color contrast for accessibility
- XSS prevention (HTTPOnly cookies)

### SMS Consent
- SMS template includes opt-out instructions
- Consent policy documented in repository
- Phone numbers validated before storage (E.164 format)

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
- Use Argon2id for password hashing

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
- **Argon2** - Secure password hashing
- **Claude (Anthropic)** - AI-assisted development

---

## 📞 Support

### Documentation
- [v1.0.0 Release Notes](CHANGELOG.md#100---2025-11-09) - Complete release details
- [API Reference](http://localhost:8000/docs) - Interactive API docs
- [Architecture Guide](docs/planning/architecture.md) - System design
- [Help & Setup](http://localhost:8000/help.html) - Twilio configuration guide

### Getting Help
1. Check the built-in Help page: `http://localhost:8000/help.html`
2. Review [CHANGELOG.md](CHANGELOG.md) for recent changes
3. Consult API documentation: `http://localhost:8000/docs`
4. Check GitHub Issues for known problems

### Known Limitations (MVP - v1.0.0)

These are intentional design choices for the MVP. Enhancements planned for future versions.

1. **Twilio Configuration via .env Only** - No UI for API key management
   - Current: API keys in `.env` file (12-factor app standard)
   - Future: Settings UI planned for v1.1.0+

2. **SMS Template Stored in LocalStorage** - Not centralized
   - Current: Each admin's browser stores template independently
   - Future: Backend API for global template (v1.1.0+)

3. **Manual Schedule Regeneration Required** - No auto-regen on team changes
   - Current: Admin must manually regenerate after team/shift changes
   - Future: Auto-regeneration with warnings (v1.2.0+)

4. **Single SMS Notification** - Only primary on-call notified
   - Current: One SMS to active on-call person
   - Future: Multi-level notifications (Primary/Secondary/Tertiary) in v1.2.0+

5. **No PTO/Vacation Management** - Manual workarounds needed
   - Current: No built-in PTO conflict detection
   - Future: PTO calendar and warnings (v1.2.0+)

See [CHANGELOG.md](CHANGELOG.md#100---2025-11-09) for complete v1.0.0 details.

---

## 🔄 Change Log

See [CHANGELOG.md](CHANGELOG.md) for complete release history.

### Version 1.0.0 (2025-11-09) - PRODUCTION RELEASE 🎉
- ✅ Authentication system with Argon2id password hashing
- ✅ Role-based access control (Admin/Viewer)
- ✅ Help & Setup page with comprehensive Twilio guide
- ✅ Same-origin architecture (frontend served from FastAPI)
- ✅ Fixed cross-origin cookie authentication bug
- ✅ 8 complete pages with live data integration
- ✅ 288 tests passing, 85% overall coverage
- ✅ Production-ready deployment

### Version 0.2.0 (2025-11-08) - MVP Backend Complete
- Complete frontend implementation (5 pages, live data)
- Rotation algorithm fix (all team members cycle through)
- 16-color system for visual clarity (WCAG AA compliant)
- Editable SMS templates with character counter
- On-call escalation chain display
- Drag-and-drop rotation ordering

### Version 0.1.0 (2025-11-06) - Core Backend
- Complete backend with 288 passing tests
- Twilio SMS integration with retry logic
- APScheduler daily notifications (8:00 AM CST)
- Complete API layer with OpenAPI docs
- Service and repository layers implemented

---

## 📊 Project Metrics (v1.0.0)

- **Total Tests:** 288 (all passing ✅)
- **Test Coverage:** 85% (exceeded 80% target!)
- **API Endpoints:** 30+ endpoints
- **Frontend Pages:** 8 complete pages
- **Documentation:** 40,000+ words
- **Team Size Support:** 1-16+ members (tested with 8)
- **Shift Flexibility:** Any number of 24h/48h shifts
- **Lines of Code:** ~15,000+ (backend + frontend + auth)
- **Password Security:** Argon2id (OWASP 2025 compliant)
- **Uptime Target:** 99.9% (APScheduler with misfire handling)

---

**Built with ❤️ by Lonnie Bruton**

*Last Updated: November 9, 2025*
*Version: 1.0.0 - Production Ready*
