# WhoseOnFirst - Setup Guide

This guide will help you set up the WhoseOnFirst project for development.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Docker Desktop** (optional, for containerization) - [Download Docker](https://www.docker.com/products/docker-desktop)
- **Twilio Account** - [Sign up for Twilio](https://www.twilio.com/try-twilio)

---

## 🚀 Initial Setup

### Step 1: Initialize Git Repository

```bash
cd /Volumes/DATA/GitHub/WhoseOnFirst

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Project documentation and setup"

# (Optional) Create main branch if not already on it
git branch -M main

# (Optional) Add remote repository
# git remote add origin https://github.com/[your-org]/WhoseOnFirst.git
# git push -u origin main
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# OR install with development dependencies
pip install -r requirements-dev.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your actual values
# On macOS:
open .env

# On Linux:
nano .env

# On Windows:
# notepad .env
```

**Required values in `.env`:**
```bash
# Get from https://console.twilio.com/
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+15551234567
```

### Step 5: Create Project Directories

```bash
# Create necessary directories
mkdir -p src/{api,models,repositories,services,scheduler,utils}
mkdir -p tests
mkdir -p frontend
mkdir -p data
mkdir -p logs
mkdir -p backups

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/api/__init__.py
touch src/models/__init__.py
touch src/repositories/__init__.py
touch src/services/__init__.py
touch src/scheduler/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

---

## 🧪 Verify Installation

### Check Python Version
```bash
python --version
# Should show: Python 3.11.x or higher
```

### Check Installed Packages
```bash
pip list
# Should show FastAPI, uvicorn, sqlalchemy, etc.
```

### Test Twilio Connection (Optional)
```bash
# Create a test script
cat > test_twilio.py << 'EOF'
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)
account = client.api.accounts(account_sid).fetch()

print(f"✓ Twilio connection successful!")
print(f"  Account: {account.friendly_name}")
print(f"  Status: {account.status}")
EOF

# Run test
python test_twilio.py

# Clean up
rm test_twilio.py
```

---

## 🐳 Docker Setup (Optional)

### Build Docker Image

```bash
# Create Dockerfile first (will be created in Phase 1)
# Then build image:
docker build -t whoseonfirst:latest .
```

### Run with Docker Compose

```bash
# Create docker-compose.yml first (will be created in Phase 1)
# Then start services:
docker-compose up -d
```

---

## 🛠️ Development Tools Setup

### Install Pre-commit Hooks

```bash
# If you installed requirements-dev.txt
pre-commit install

# Test hooks
pre-commit run --all-files
```

### Configure VS Code (Optional)

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### Configure PyCharm (Optional)

1. Open project in PyCharm
2. Set Python interpreter to `venv/bin/python`
3. Enable Black formatter: Preferences → Tools → Black
4. Enable Flake8: Preferences → Tools → External Tools

---

## 📚 Next Steps

### Phase 1 Development Checklist

- [ ] Review [PRD.md](docs/planning/PRD.md)
- [ ] Review [Architecture](docs/planning/architecture.md)
- [ ] Set up project structure (src/, tests/, frontend/)
- [ ] Create database models
- [ ] Implement API endpoints
- [ ] Set up APScheduler
- [ ] Integrate Twilio SMS
- [ ] Build admin interface
- [ ] Write tests
- [ ] Create Dockerfile
- [ ] Deploy to test environment

### Recommended Reading Order

1. [PRD.md](docs/planning/PRD.md) - Understand requirements
2. [Research Notes](docs/planning/research-notes.md) - Understand technology choices
3. [Technical Stack](docs/planning/technical-stack.md) - Understand implementation details
4. [Architecture](docs/planning/architecture.md) - Understand system design

---

## 🔧 Common Issues

### Issue: Python version too old

**Solution:**
```bash
# On macOS with Homebrew
brew install python@3.11

# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11

# On RHEL/CentOS
sudo dnf install python3.11
```

### Issue: Twilio authentication fails

**Solution:**
1. Verify credentials at https://console.twilio.com/
2. Check that `.env` file has correct values
3. Ensure no extra spaces in `.env` values
4. Verify phone number is in E.164 format (+15551234567)

### Issue: Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

### Issue: Database locked (SQLite)

**Solution:**
```bash
# Stop the application
# Check for stale connections
fuser data/whoseonfirst.db

# If necessary, remove journal files
rm data/whoseonfirst.db-journal
```

---

## 🧹 Cleanup

If you need to start fresh:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove database files
rm -rf data/*.db

# Remove logs
rm -rf logs/*.log

# Remove cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Keep: .env, .git, docs/, src/
```

---

## 📞 Getting Help

If you encounter issues:

1. Check the [documentation](docs/)
2. Review error messages carefully
3. Search GitHub issues (once repository is created)
4. Contact project lead

---

## 🎯 Success Criteria

You'll know setup is complete when:

- ✅ Git repository is initialized
- ✅ Virtual environment is created and activated
- ✅ All dependencies are installed (`pip list` shows packages)
- ✅ `.env` file is configured with Twilio credentials
- ✅ Project directories are created
- ✅ Twilio connection test passes (optional)
- ✅ You've reviewed the documentation
- ✅ You're ready to start Phase 1 development!

---

## 📝 Notes

- **Never commit `.env`** - It contains sensitive credentials
- **Always work in virtual environment** - Keeps dependencies isolated
- **Update documentation** - As you make changes
- **Write tests** - Aim for >80% coverage
- **Use type hints** - Helps catch bugs early

---

**Ready to start coding? Let's build WhoseOnFirst! 🚀**

*Last Updated: November 4, 2025*
