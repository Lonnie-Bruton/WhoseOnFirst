# Development Workflow Guide

Quick reference for common development tasks and workflows.

---

## 🚀 Starting Development

```bash
# Navigate to project
cd /Volumes/DATA/GitHub/WhoseOnFirst

# Activate virtual environment
source venv/bin/activate

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open in browser
# http://localhost:8000/docs  (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

## 🧪 Testing Workflow

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_rotation_algorithm.py

# Run specific test
pytest tests/test_rotation_algorithm.py::test_fair_rotation

# Run with verbose output
pytest -v -s

# Run only failed tests from last run
pytest --lf
```

---

## 🎨 Code Quality

```bash
# Format code with Black
black .

# Sort imports
isort .

# Lint with Flake8
flake8 src/ tests/

# Type check with MyPy
mypy src/

# Run all quality checks
black . && isort . && flake8 src/ && mypy src/
```

---

## 💾 Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history

# Reset database (CAUTION: destroys data)
rm data/whoseonfirst.db
alembic upgrade head
```

---

## 🐳 Docker Workflow

```bash
# Build image
docker build -t whoseonfirst:latest .

# Run container (development)
docker run -d \
  --name whoseonfirst-dev \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  whoseonfirst:latest

# View logs
docker logs -f whoseonfirst-dev

# Stop container
docker stop whoseonfirst-dev

# Remove container
docker rm whoseonfirst-dev

# Docker Compose (when available)
docker-compose up -d
docker-compose down
docker-compose logs -f
```

---

## 📝 Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Stage changes
git add .

# Commit with message
git commit -m "feat: add rotation algorithm"

# Push to remote
git push origin feature/your-feature-name

# Update from main
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main

# View status
git status

# View diff
git diff
```

### Commit Message Convention

```
feat: Add new feature
fix: Fix a bug
docs: Documentation changes
style: Code style changes (formatting)
refactor: Code refactoring
test: Add or update tests
chore: Maintenance tasks
```

---

## 🔍 Debugging

### Using IPython
```bash
# Start IPython shell
ipython

# Import and test code
from src.services.rotation_algorithm import FairRotationAlgorithm
# ... test your code
```

### Using IPdb (Debugger)
```python
# In your code, add breakpoint
import ipdb; ipdb.set_trace()

# Run code, debugger will stop at breakpoint
# Common commands:
# n - next line
# s - step into function
# c - continue
# p variable - print variable
# l - list code around current line
# q - quit debugger
```

### View Application Logs
```bash
# Tail application logs
tail -f logs/whoseonfirst.log

# View last 100 lines
tail -n 100 logs/whoseonfirst.log

# Search logs
grep "ERROR" logs/whoseonfirst.log
```

---

## 📞 Twilio Testing

### Send Test SMS via Python
```python
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

message = client.messages.create(
    body="Test message from WhoseOnFirst",
    from_=os.getenv('TWILIO_PHONE_NUMBER'),
    to="+15551234567"  # Your phone number
)

print(f"Message SID: {message.sid}")
```

### Check Message Status
```python
message = client.messages(message_sid).fetch()
print(f"Status: {message.status}")
```

---

## 🔄 API Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# List team members
curl http://localhost:8000/api/v1/team-members/

# Create team member
curl -X POST http://localhost:8000/api/v1/team-members/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "+15551234567"}'

# Get current schedule
curl http://localhost:8000/api/v1/schedule/current
```

### Using HTTPie (if installed)
```bash
# Health check
http http://localhost:8000/health

# Create team member
http POST http://localhost:8000/api/v1/team-members/ \
  name="John Doe" \
  phone="+15551234567"
```

---

## 📊 Performance Testing

### Using Apache Bench
```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/health
```

### Using wrk
```bash
# 30 second test, 10 threads, 100 connections
wrk -t10 -c100 -d30s http://localhost:8000/api/v1/schedule/current
```

---

## 🧹 Maintenance Tasks

### Clean Python Cache
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
```

### Clean Logs (keep last 7 days)
```bash
find logs/ -name "*.log" -mtime +7 -delete
```

### Backup Database
```bash
# Manual backup
cp data/whoseonfirst.db backups/whoseonfirst_$(date +%Y%m%d_%H%M%S).db

# Compress backup
gzip backups/whoseonfirst_$(date +%Y%m%d_%H%M%S).db
```

### Update Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi
```

---

## 📱 Claude-Code CLI Workflow

### Starting a Coding Session
```bash
# From project root
claude-code

# Claude-Code will analyze the project context
# Give it specific tasks like:
# "Implement the TeamMemberService class"
# "Add tests for the rotation algorithm"
# "Create the API endpoint for schedule generation"
```

### Best Practices with Claude-Code
1. **Be specific** - "Add POST endpoint for creating team members with validation"
2. **Reference documentation** - "Following the architecture in docs/planning/architecture.md"
3. **Request tests** - "Include unit tests with >80% coverage"
4. **Ask for reviews** - "Review this code for security issues"

---

## 🎯 Daily Development Checklist

### Morning Routine
- [ ] Pull latest changes: `git pull origin main`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Check for dependency updates: `pip list --outdated`
- [ ] Review PRD and current sprint tasks
- [ ] Start development server

### Before Committing
- [ ] Run tests: `pytest`
- [ ] Check code quality: `black . && flake8 src/`
- [ ] Type check: `mypy src/`
- [ ] Review changes: `git diff`
- [ ] Update documentation if needed
- [ ] Write meaningful commit message

### End of Day
- [ ] Commit work in progress (if stable)
- [ ] Push to feature branch
- [ ] Update task board / notes
- [ ] Backup database: `cp data/whoseonfirst.db backups/`

---

## 🚨 Emergency Procedures

### Application Won't Start
```bash
# Check port availability
lsof -i :8000

# Check Python version
python --version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check environment variables
cat .env

# View recent logs
tail -n 50 logs/whoseonfirst.log
```

### Database Corruption
```bash
# Stop application
# Restore from backup
cp backups/whoseonfirst_LATEST.db data/whoseonfirst.db

# Or rebuild from migrations
rm data/whoseonfirst.db
alembic upgrade head
```

### Twilio API Issues
```bash
# Check Twilio status
# Visit: https://status.twilio.com/

# Verify credentials
python test_twilio.py

# Check rate limits in Twilio Console
# https://console.twilio.com/
```

---

## 📚 Useful Links

### Project Documentation
- [PRD](docs/planning/PRD.md)
- [Architecture](docs/planning/architecture.md)
- [Tech Stack](docs/planning/technical-stack.md)
- [Research Notes](docs/planning/research-notes.md)

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [APScheduler Docs](https://apscheduler.readthedocs.io/)
- [Twilio Python Docs](https://www.twilio.com/docs/libraries/python)
- [Pytest Docs](https://docs.pytest.org/)

### API Documentation (when running)
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 💡 Pro Tips

1. **Use tab completion** in IPython for exploring APIs
2. **Keep .env up to date** when adding new config options
3. **Write tests first** (TDD) for complex logic
4. **Use type hints** everywhere for better IDE support
5. **Check coverage** after writing tests: `pytest --cov`
6. **Review architecture docs** before major changes
7. **Update documentation** alongside code changes
8. **Commit often** with meaningful messages
9. **Use branches** for features, never commit to main
10. **Ask Claude** for help via Claude-Code CLI!

---

**Happy Coding! 🎉**

*Last Updated: November 4, 2025*
