# WhoseOnFirst

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/version-1.5.0-success.svg)](CHANGELOG.md)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b37c9c41b9644a9990be09eeda5bf014)](https://app.codacy.com/gh/Lonnie-Bruton/WhoseOnFirst/dashboard)

Automated on-call rotation and SMS notification system for the technical support team.

---

## Overview

WhoseOnFirst manages shift assignments and sends daily SMS notifications to on-call team members. The system uses a simple circular rotation to ensure fair, predictable shift distribution across the team.

**Key Features:**
- Role-based access control (Admin/Viewer)
- Configurable 24-hour and 48-hour shifts
- Automated 8:00 AM CST daily notifications via Twilio
- Manual schedule overrides for vacation/sick coverage
- Drag-and-drop rotation ordering
- Weekly escalation contact summaries

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI, Python 3.12 |
| Database | SQLite with SQLAlchemy ORM |
| Scheduler | APScheduler |
| SMS | Twilio |
| Frontend | Vanilla JS, Tabler CSS |
| Container | Red Hat UBI9 (OpenShift compatible) |

---

## Usage

### Access

- **URL:** `http://localhost:8900/` (dev) or `http://localhost:8000/` (prod)
- **Default Admin:** `admin` / `Admin123!`
- **Default Viewer:** `viewer` / `Viewer123!`

*Change passwords immediately after first login.*

### Pages

| Page | Access | Purpose |
|------|--------|---------|
| Dashboard | All | Current on-call, escalation chain, calendar |
| Team Members | Admin | Add/edit members, drag-drop rotation order |
| Shift Configuration | Admin | Configure shift durations and days |
| Schedule Generation | Admin | Generate rotation schedules |
| Schedule Overrides | Admin | Manual coverage for vacation/sick |
| Notifications | Admin | SMS history and template editing |
| Help | All | Twilio setup guide |

### Docker

```bash
# Development (port 8900)
docker-compose -f docker-compose.dev.yml up -d

# Production (port 8000)
docker-compose up -d
```

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Twilio](https://www.twilio.com/) - SMS delivery
- [Tabler](https://tabler.io/) - UI components
- [Claude](https://claude.ai/) - AI-assisted development

---

*Version 1.5.0 · [Changelog](CHANGELOG.md)*
