# WhoseOnFirst - On-Call Team SMS Notifier

> Automated on-call rotation and SMS notification system for technical teams

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-blue.svg)](docs/planning/PRD.md)
[![Progress](https://img.shields.io/badge/progress-25%25-blue.svg)](CHANGELOG.md)

---

## 🎯 Overview

WhoseOnFirst is an automated scheduling and notification system that manages fair on-call rotations for technical teams. The system ensures equitable shift distribution using simple circular rotation, schedules the 48-hour double shift during the workweek (Tue-Wed) to minimize weekend impact, and automatically notifies on-call personnel via SMS at the start of each shift.

### Key Features

- 📅 **Simple Circular Rotation** - Fair, predictable rotation where everyone moves forward one position each week
- 📱 **Automated SMS Notifications** - Daily 8:00 AM CST notifications via Twilio
- ⚙️ **Flexible Shift Patterns** - Support for 24-hour and 48-hour shifts
- 🖥️ **Simple Admin Interface** - Web-based dashboard for schedule management
- 🐳 **Docker Ready** - Containerized for easy deployment on RHEL 10

---

## 📋 Project Status

**Current Phase:** Phase 1 Development (Week 1-2)
**Progress:** ~25% Complete (Database + Repository Layer)
**Target Beta:** 30-90 days
**Version:** 0.2.0 (Pre-Alpha)

### Documentation

- [Product Requirements Document (PRD)](docs/planning/PRD.md) - Complete requirements and specifications
- [Research Notes](docs/planning/research-notes.md) - Technology research and decision rationale
- [Technical Stack](docs/planning/technical-stack.md) - Detailed technology choices and architecture
- [Architecture Overview](docs/planning/architecture.md) - System design and data flow diagrams

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI 0.115+ | REST API framework with auto-documentation |
| **Server** | Uvicorn | High-performance ASGI server |
| **Scheduler** | APScheduler 3.10+ | Cron-based job scheduling |
| **Database** | SQLite → PostgreSQL | Embedded DB (Phase 1) → Enterprise DB (Phase 2+) |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction layer |
| **SMS** | Twilio Python SDK | SMS delivery service |
| **Frontend** | Vanilla JS + HTML/CSS | Simple web interface |

---

## 🚀 Quick Start

> **Note:** Project is currently in planning phase. Implementation begins in Phase 1.

### Prerequisites

- Python 3.11 or higher
- Docker Desktop (for containerization)
- Twilio account with phone number
- Git

### Installation (Planned)

```bash
# Clone repository
git clone https://github.com/[org]/WhoseOnFirst.git
cd WhoseOnFirst

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Twilio credentials

# Initialize database
alembic upgrade head

# Run development server
uvicorn main:app --reload
```

### Docker Deployment (Planned)

```bash
# Build image
docker build -t whoseonfirst:latest .

# Run container
docker run -d \
  --name whoseonfirst \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  whoseonfirst:latest
```

---

## 📖 Usage

### Admin Dashboard

Access the web interface at `http://localhost:8000`

**Features:**
- View current week's on-call schedule
- Manage team members (add/remove/edit)
- Configure shift patterns
- View notification history
- Manual schedule overrides

### API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example API Calls

```bash
# Get current week schedule
curl http://localhost:8000/api/v1/schedule/current

# Add team member
curl -X POST http://localhost:8000/api/v1/team-members/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "+15551234567"}'

# Send test notification
curl -X POST http://localhost:8000/api/v1/notifications/send-test \
  -H "Content-Type: application/json" \
  -d '{"team_member_id": 1, "message": "Test notification"}'
```

---

## 🗓️ Development Roadmap

### Phase 1: MVP (Weeks 1-6) 🚧 *In Progress* (~25% Complete)
- [x] Requirements gathering and PRD
- [x] Technology research and stack selection
- [x] Architecture design
- [x] Database models and migrations (4 tables, 20+ indexes)
- [x] Repository layer (5 repositories, 1,447 lines)
- [ ] Service layer (business logic) - *Next*
- [ ] API endpoints (FastAPI routes)
- [ ] Scheduling logic and rotation algorithm
- [ ] Twilio SMS integration
- [ ] Basic admin interface
- [ ] Docker containerization
- [ ] Test suite with 80%+ coverage

### Phase 2: Enhancement (Weeks 7-10) 📋 *Planned*
- [ ] Multi-user authentication
- [ ] Enhanced UI/UX
- [ ] Email notification backup
- [ ] Advanced reporting
- [ ] Performance optimization

### Phase 3: Integration (Weeks 11-14) 💭 *Future*
- [ ] Microsoft Teams integration
- [ ] REST API for external systems
- [ ] Calendar export (iCal)
- [ ] Webhook support

### Phase 4: Scale (Weeks 15+) 🔮 *Vision*
- [ ] Multi-team support
- [ ] PostgreSQL migration
- [ ] Mobile application
- [ ] Advanced analytics

---

## 🏗️ Project Structure

```
WhoseOnFirst/
├── docs/                    # Documentation
│   ├── planning/           # Planning documents
│   │   ├── PRD.md
│   │   ├── research-notes.md
│   │   ├── technical-stack.md
│   │   └── architecture.md
│   ├── api/                # API documentation
│   └── deployment/         # Deployment guides
├── src/                    # Source code (to be created)
│   ├── main.py            # FastAPI application entry point
│   ├── api/               # API routes
│   ├── services/          # Business logic
│   ├── models/            # Database models
│   ├── repositories/      # Data access layer
│   ├── scheduler/         # APScheduler configuration
│   └── utils/             # Utility functions
├── tests/                 # Test suite (to be created)
├── frontend/              # Web interface (to be created)
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore patterns
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose for development
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_rotation_algorithm.py

# Run with verbose output
pytest -v
```

---

## 🔒 Security

### Credential Management
- All secrets stored in `.env` file (never committed to Git)
- Twilio credentials stored as environment variables
- Database files have restricted permissions (600)

### Best Practices
- Input validation on all API endpoints
- SQL injection prevention via SQLAlchemy ORM
- Phone numbers sanitized in logs
- HTTPS enforced in production
- Regular security updates

**Report security vulnerabilities to:** [security contact TBD]

---

## 🤝 Contributing

This is currently an internal project. Contributing guidelines will be added if the project is open-sourced.

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push branch: `git push origin feature/your-feature`
4. Create pull request

### Code Standards
- Follow PEP 8 style guide
- Use type hints for all functions
- Maintain >80% test coverage
- Update documentation for API changes

---

## 📝 License

[License TBD - To be determined by organization]

---

## 🙏 Acknowledgments

- **Twilio** - SMS delivery platform
- **FastAPI** - Modern web framework
- **APScheduler** - Reliable job scheduling
- **SQLAlchemy** - Excellent ORM
- **Claude (Anthropic)** - AI-assisted development and project management

---

## 📞 Support

### Documentation
- [Full Documentation](docs/)
- [API Reference](http://localhost:8000/docs)
- [Architecture Guide](docs/planning/architecture.md)

### Contact
- Project Lead: [TBD]
- Team Email: [TBD]

---

## 🔄 Change Log

### Version 0.1.0 (2025-11-04)
- Initial project setup
- Comprehensive planning documentation
- Technology stack selection
- Architecture design

---

## 🎓 Learning Resources

If you're new to the technologies used in this project:

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Twilio Python Quickstart](https://www.twilio.com/docs/sms/quickstart/python)
- [Docker Getting Started](https://docs.docker.com/get-started/)

---

## 📊 Project Metrics

- **Lines of Code:** TBD (not yet implemented)
- **Test Coverage:** Target 80%+
- **Documentation:** ~15,000 words (planning phase)
- **Estimated Team Members Supported:** 5-10 (Phase 1), 100+ (Future)

---

**Built with ❤️ by the [Your Team] team**

*Last Updated: November 4, 2025*
