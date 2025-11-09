# Current Sprint - Phase 2: Docker & Offline Installer

> **Sprint Goal:** Create production-ready Docker/Podman deployment with offline installer  
> **Start Date:** 2025-11-09  
> **Est. Completion:** 2025-11-16 (1 week)  
> **Assigned To:** Claude Code CLI  
> **Blocked By:** None (Twilio approval not required for containerization)

---

## Sprint Overview

While waiting for Twilio US number approval, we're building the Docker/Podman containerization and offline installer bundle. This enables immediate deployment to corporate RHEL VM once Twilio is approved.

**Why This Sprint:**
- Corporate deployment requires air-gapped installer (firewall restrictions)
- RHEL environment prefers Podman over Docker
- Testing environment (Proxmox RHEL-10 VM) is ready
- No external blockers - can work fully offline

---

## Tasks

### 🎯 Priority 1: Docker/Podman Containerization

#### Task 1.1: Create Multi-Stage Dockerfile
**Est: 2 hours** | **Status:** Not Started

```dockerfile
# Requirements:
- Stage 1: Builder (Python deps, compile assets)
- Stage 2: Runtime (minimal image, only what's needed)
- Base image: python:3.11-slim or ubi9/python-311 (RHEL-compatible)
- Copy only src/, frontend/, alembic/, requirements.txt
- Install dependencies with --no-cache-dir
- Set working directory to /app
- Expose port 8000
- Health check endpoint
- Non-root user for security
- Environment variables from .env
```

**Files to create:**
- `Dockerfile`

**Acceptance criteria:**
- Image builds successfully
- Image size < 500MB
- Health check passes
- Runs as non-root user

---

#### Task 1.2: Create docker-compose.yml / podman-compose.yml
**Est: 1 hour** | **Status:** Not Started

```yaml
# Requirements:
- Service: whoseonfirst-app
- Volume mounts: ./data:/app/data (database persistence)
- Volume mounts: ./logs:/app/logs (log persistence)
- Volume mounts: ./backups:/app/backups (backup storage)
- Environment file: .env
- Port mapping: 8000:8000
- Restart policy: unless-stopped
- Health check with retries
```

**Files to create:**
- `docker-compose.yml`
- `podman-compose.yml` (if different from docker-compose)

**Acceptance criteria:**
- Starts with `docker-compose up -d` or `podman-compose up -d`
- Database persists after container restart
- Logs accessible on host
- Stops gracefully with SIGTERM

---

#### Task 1.3: Update .env.example
**Est: 30 min** | **Status:** Not Started

```bash
# Add container-specific vars:
- DATABASE_URL (for container path)
- CONTAINER_TIMEZONE=America/Chicago
- UVICORN_WORKERS=2
- UVICORN_HOST=0.0.0.0
- UVICORN_PORT=8000
```

**Files to update:**
- `.env.example`

**Acceptance criteria:**
- All required vars documented
- Example values provided
- Comments explain each variable

---

### 🎯 Priority 2: Offline Installer Bundle

#### Task 2.1: Create Image Save/Load Scripts
**Est: 1 hour** | **Status:** Not Started

**Files to create:**
- `scripts/build-offline-bundle.sh` - Saves images to .tar files
- `scripts/load-images.sh` - Loads .tar files into Podman/Docker

```bash
# build-offline-bundle.sh requirements:
- Build whoseonfirst:latest image
- Save to whoseonfirst-app.tar
- Pull and save any base images
- Create SHA256 checksums for verification
- Bundle into offline-installer/ directory

# load-images.sh requirements:
- Verify checksums
- Load all .tar files
- Verify images loaded successfully
- List loaded images for confirmation
```

**Acceptance criteria:**
- Can build bundle on internet-connected machine
- Can load bundle on air-gapped machine
- Checksums verify integrity

---

#### Task 2.2: Vendor Python Dependencies
**Est: 1 hour** | **Status:** Not Started

**Files to create:**
- `scripts/vendor-python-deps.sh` - Download all Python packages

```bash
# Requirements:
- Create vendor/python-deps/ directory
- pip download -r requirements.txt -d vendor/python-deps
- Include all transitive dependencies
- Works offline with --no-index --find-links
```

**Files to update:**
- `Dockerfile` - Add COPY vendor/ and pip install from local

**Acceptance criteria:**
- No internet required during container build
- All dependencies install successfully
- Requirements.txt remains unchanged

---

#### Task 2.3: Self-Host Frontend Assets (Optional)
**Est: 2 hours** | **Status:** Not Started

**Decision Point:** Do we need fully offline frontend?
- **Option A:** Keep CDN links (user browser needs internet)
- **Option B:** Self-host all assets (fully air-gapped)

**If Option B:**
```bash
# Download to frontend/assets/:
- Tabler CSS/JS
- Tabler icons
- SortableJS
- Any other CDN resources
```

**Files to update:**
- All `frontend/*.html` files - Update CDN links to `/assets/`
- `src/main.py` - Add static file mount for `/assets`

**Acceptance criteria:**
- No external CDN requests
- All assets load offline
- Page functionality unchanged

---

### 🎯 Priority 3: Installation Scripts

#### Task 3.1: Create install.sh
**Est: 2 hours** | **Status:** Not Started

**Files to create:**
- `scripts/install.sh` - Main installation script

```bash
# Requirements:
- Check if Podman/Docker installed
- Load container images from offline bundle
- Create /opt/whoseonfirst directory structure
- Copy config files (.env.example → .env)
- Set up data directories with permissions
- Create systemd service file
- Enable and start service
- Display post-install instructions
- Health check verification
```

**Acceptance criteria:**
- Runs without user interaction (except .env config)
- Idempotent (safe to run multiple times)
- Clear error messages
- Rollback on failure

---

#### Task 3.2: Create Systemd Service
**Est: 1 hour** | **Status:** Not Started

**Files to create:**
- `scripts/systemd/whoseonfirst.service`

```ini
# Requirements:
[Unit]
Description=WhoseOnFirst On-Call Rotation System
After=network.target

[Service]
Type=forking
User=whoseonfirst
WorkingDirectory=/opt/whoseonfirst
ExecStart=/usr/bin/podman-compose up -d
ExecStop=/usr/bin/podman-compose down
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

**Acceptance criteria:**
- Starts on boot
- Restarts on failure
- Stops gracefully on shutdown
- Status shows correct state

---

#### Task 3.3: Create Backup/Restore Scripts
**Est: 2 hours** | **Status:** Not Started

**Files to create:**
- `scripts/backup.sh` - Backup database and config
- `scripts/restore.sh` - Restore from backup

```bash
# backup.sh requirements:
- Stop container (or use SQLite backup API)
- Copy database to backups/ with timestamp
- Copy .env file (sanitized)
- Create backup manifest (versions, date, size)
- Compress with gzip
- Verify backup integrity

# restore.sh requirements:
- Stop container
- Verify backup integrity
- Restore database
- Restore config (prompt for secrets)
- Start container
- Verify health
```

**Acceptance criteria:**
- Backup completes in < 1 min
- Restore works from any backup
- No data loss
- Logs all operations

---

#### Task 3.4: Create uninstall.sh
**Est: 1 hour** | **Status:** Not Started

**Files to create:**
- `scripts/uninstall.sh` - Clean uninstall

```bash
# Requirements:
- Stop systemd service
- Disable systemd service
- Remove container and images
- Prompt to keep/remove data
- Remove /opt/whoseonfirst (if requested)
- Display what was removed
```

**Acceptance criteria:**
- Removes all traces
- Option to preserve data
- Cannot be run accidentally
- Logs all deletions

---

### 🎯 Priority 4: Documentation

#### Task 4.1: Create DEPLOYMENT.md
**Est: 2 hours** | **Status:** Not Started

**Files to create:**
- `docs/DEPLOYMENT.md`

```markdown
# Content:
1. Prerequisites (RHEL 10, Podman, permissions)
2. Offline installer usage
   - Extract bundle
   - Run install.sh
   - Configure .env
   - Verify installation
3. Manual Docker/Podman deployment
4. Systemd service management
5. Backup/restore procedures
6. Troubleshooting guide
7. Firewall configuration
8. SELinux considerations
9. Monitoring recommendations
```

**Acceptance criteria:**
- Step-by-step with screenshots
- Covers common errors
- Tested on clean RHEL VM
- IT team can follow without help

---

#### Task 4.2: Create IT Handoff Package README
**Est: 1 hour** | **Status:** Not Started

**Files to create:**
- `IT-HANDOFF-README.md` (in offline bundle root)

```markdown
# Content:
1. What is WhoseOnFirst?
2. System requirements
3. Quick start (3 steps)
4. Support contacts
5. License information
```

**Acceptance criteria:**
- Fits on one page
- Non-technical language
- Clear next steps

---

### 🎯 Priority 5: Testing

#### Task 5.1: Test on Proxmox RHEL-10 VM
**Est: 4 hours** | **Status:** Not Started

**Test plan:**
```
1. Create clean RHEL-10 VM in Proxmox
2. Disable internet (simulate air-gap)
3. Copy offline bundle via USB/network share
4. Run install.sh
5. Configure .env with Twilio credentials
6. Verify:
   - Container starts
   - Database initializes
   - Web UI accessible
   - API responds
   - Scheduler starts
   - Health checks pass
7. Reboot VM
8. Verify auto-start works
9. Test backup/restore
10. Test uninstall
```

**Acceptance criteria:**
- Installation completes without internet
- All features work
- Survives reboot
- Backup/restore successful

---

#### Task 5.2: Create Deployment Checklist
**Est: 30 min** | **Status:** Not Started

**Files to create:**
- `docs/DEPLOYMENT-CHECKLIST.md`

```markdown
# Pre-deployment:
- [ ] Twilio account verified
- [ ] .env configured with secrets
- [ ] Team members added
- [ ] Shifts configured
- [ ] Test schedule generated
- [ ] Test SMS sent successfully

# Deployment:
- [ ] Offline bundle created
- [ ] Transferred to RHEL VM
- [ ] Install.sh executed
- [ ] Systemd service enabled
- [ ] Health checks passing

# Post-deployment:
- [ ] First scheduled SMS delivered
- [ ] Logs show no errors
- [ ] Backup cron job configured
- [ ] Monitoring alerts set up
- [ ] IT team trained
```

**Acceptance criteria:**
- Covers all critical steps
- Print-friendly format
- Sign-off column for audits

---

## Definition of Done

Sprint is complete when:

- ✅ Docker/Podman images build successfully
- ✅ docker-compose.yml / podman-compose.yml working
- ✅ Offline installer bundle created
- ✅ All Python dependencies vendored
- ✅ install.sh completes on clean RHEL VM
- ✅ Systemd service auto-starts on boot
- ✅ Backup/restore scripts working
- ✅ DEPLOYMENT.md comprehensive
- ✅ Full air-gapped install tested in Proxmox
- ✅ IT handoff package ready

---

## Out of Scope for This Sprint

- ❌ Authentication (Phase 2, separate sprint)
- ❌ HTTPS/SSL (Phase 2, after auth)
- ❌ Nginx reverse proxy (Phase 2, after auth)
- ❌ Shift override features (Phase 3)
- ❌ Multi-level SMS (Phase 3)
- ❌ PostgreSQL migration (Phase 4)

---

## Notes for Claude Code

**Working Directory:** `/Volumes/DATA/GitHub/WhoseOnFirst`

**Test Commands:**
```bash
# Build Docker image
docker build -t whoseonfirst:latest .

# Test with docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down

# Build offline bundle
./scripts/build-offline-bundle.sh

# Test on clean VM (in Proxmox)
# 1. scp offline-installer.tar.gz to VM
# 2. tar -xzf offline-installer.tar.gz
# 3. cd offline-installer
# 4. ./install.sh
```

**Key Files to Read First:**
- `requirements.txt` - Python dependencies
- `src/main.py` - Entry point, understand startup
- `.env.example` - Environment variables
- `alembic/` - Database migrations

**Remember:**
- Update CHANGELOG.md with each commit
- Run pytest before committing
- Test in Proxmox before marking complete
- Ask questions if requirements unclear
