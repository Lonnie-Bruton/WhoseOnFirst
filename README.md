# WhoseOnFirst - On-Call Team SMS Notifier

> Automated on-call rotation and SMS notification system for technical teams

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-success.svg)](https://github.com/Lonnie-Bruton/WhoseOnFirst/releases/tag/v1.0.0)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](CHANGELOG.md)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b37c9c41b9644a9990be09eeda5bf014)](https://app.codacy.com/gh/Lonnie-Bruton/WhoseOnFirst/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

---

## 🎯 Overview

WhoseOnFirst is a production-ready on-call rotation and SMS notification system that manages shift assignments for technical teams. The system ensures equitable shift distribution using simple circular rotation. 
### Key Features

- 🔐 **Secure Authentication** - Role-based access control (Admin/Viewer) with Argon2id password hashing
- 📅 **Simple Circular Rotation** - Fair, predictable rotation where all team members cycle through continuously
- 📱 **Automated SMS Notifications** - Shift start notifications via Twilio
- ⚙️ **Flexible Shift Patterns** - Support for 24-hour and 48-hour shifts with visual coverage timeline
- 🔄 **Dynamic Team Management** - Drag-and-drop rotation ordering, works with any team size

---

## 📋 Project Status

**Current Version:** 1.0.0 🎉
**Status:** Production Ready - MVP Complete
**Release Date:** November 9, 2025
**Next Phase:** Docker containerization for RHEL deployment

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
| **Database** | SQLite | Embedded DB (MVP) |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction with Alembic migrations |
| **SMS** | Twilio Python SDK | SMS delivery service with retry logic |
| **Auth** | Argon2-CFFI | Password hashing (OWASP 2025 recommended) |
| **Frontend** | Vanilla JS + Tabler CSS | Responsive web interface (no build step) |

## 📖 Usage

### Web Interface

Access at `http://localhost:8900/` and login with default credentials:
- **Admin**: username=`admin`, password=`Admin123!` (full access)
- **Viewer**: username=`viewer`, password=`Viewer123!` (read-only)

⚠️ **IMPORTANT:** Change the admin and viewer password immediately after first login!

**Available Pages:**
1. **Dashboard** - Current on-call status, escalation chain, monthly calendar with phone numbers
2. **Team Members** - Add/edit/reorder team members, drag-and-drop rotation order (Admin only)
3. **Shift Configuration** - Configure 24h/48h shifts, visual coverage timeline (Admin only)
4. **Schedule Generation** - Generate 1-104 weeks of rotation, 14-day preview (Admin only)
5. **Notifications** - SMS history, delivery stats, editable message template (Admin only)
6. **Help & Setup** - Comprehensive Twilio configuration guide with troubleshooting (All users)
7. **Change Password** - Password management for admin and viewer users
8. **Login** - Secure authentication with branded design

---

## 🤝 Contributing

This is currently a private internal project, but feel free to clone and make it your own!

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

*Last Updated: November 9, 2025*
*Version: 1.0.0 - Production Ready*
