# WhoseOnFirst Project Roadmap

> **Last Updated:** 2025-11-09  
> **Current Phase:** Phase 2 (Deployment & Auth) - IN PLANNING

---

## Phase 1: MVP ✅ COMPLETE (Nov 2024 - Nov 2025)

**Status:** 100% Complete  
**Duration:** ~6 weeks actual development  
**Outcome:** Fully functional on-call rotation system with SMS notifications

### Backend (All Complete ✅)

- [x] Database models with SQLAlchemy (team_members, shifts, schedule, notification_log)
- [x] Repository layer (BaseRepository + 5 specialized repositories)
- [x] Service layer (5 services with business logic)
- [x] Circular rotation algorithm (100% test coverage)
- [x] FastAPI REST API (15+ endpoints)
- [x] APScheduler integration (8:00 AM CST daily job)
- [x] Twilio SMS integration with retry logic
- [x] Notification logging and audit trail
- [x] Rotation order management (drag-drop support)
- [x] 288 tests with 85% coverage

### Frontend (All Complete ✅)

- [x] Dashboard with live calendar and escalation chain
- [x] Team member management with drag-drop reordering
- [x] Shift configuration with weekly coverage timeline
- [x] Schedule generation with 14-day preview
- [x] Notifications history and SMS template editor
- [x] Tabler.io responsive design
- [x] 16-color WCAG AA compliant color system

### Discoveries & Decisions 💡

- **Podman over Kubernetes** - Right-sized for 7-person team, RHEL-native
- **Rotation order field** - Added to support manual ordering vs purely algorithmic
- **48-hour shift display fix** - Required date range checking for multi-day spans
- **Phone uniqueness disabled** - Temporary for testing, must re-enable before production
- **LocalStorage for SMS templates** - MVP solution, migrate to backend in Phase 3

### Known Issues 🔴

- **Twilio Verification Pending** - Awaiting US number approval (~1 week)
- **Phone constraint disabled** - Migration `200f01c20965` must be reverted before production
- **No authentication** - Open system, planned for Phase 2
- **SQLite only** - PostgreSQL migration planned for Phase 4

---

## Phase 2: Deployment & Auth 🔄 IN PLANNING (Dec 2024 - Jan 2025)

**Status:** Planning & Research  
**Goal:** Production-ready deployment on corporate RHEL VM with authentication

### Deployment (Priority)

- [ ] Docker/Podman containerization
  - [ ] Multi-stage Dockerfile (build + runtime)
  - [ ] docker-compose.yml / podman-compose.yml
  - [ ] Volume mounts for data persistence
  - [ ] Environment variable configuration
  - [ ] Health check endpoints
- [ ] Offline installer bundle (air-gapped deployment)
  - [ ] Pre-downloaded container images (podman save/load)
  - [ ] Vendored Python dependencies (pip download)
  - [ ] Self-hosted frontend assets (no CDN)
  - [ ] Installation scripts (install.sh, uninstall.sh)
  - [ ] Systemd service files
  - [ ] Backup/restore scripts
- [ ] Testing on Proxmox RHEL-10 lab
  - [ ] Full offline install test
  - [ ] Systemd auto-start verification
  - [ ] Firewall configuration
  - [ ] SELinux compatibility
- [ ] Production deployment to corporate RHEL VM
  - [ ] IT handoff package (docs + installer)
  - [ ] Deployment guide with screenshots
  - [ ] Rollback procedures
  - [ ] Monitoring setup

### Authentication (After Deployment)

- [ ] User authentication system
  - [ ] JWT token-based auth
  - [ ] Login/logout endpoints
  - [ ] Password hashing (bcrypt)
  - [ ] Session management
- [ ] Role-based access control (RBAC)
  - [ ] Admin role (full access)
  - [ ] Member role (view-only)
  - [ ] Team lead role (manage own team)
- [ ] Frontend login page
  - [ ] Login form with validation
  - [ ] Protected routes
  - [ ] Token storage (httpOnly cookies)
  - [ ] Auto-logout on expiration

### HTTPS Support

- [ ] TLS/SSL certificate setup
  - [ ] Let's Encrypt or corporate CA
  - [ ] Certificate renewal automation
- [ ] Nginx reverse proxy
  - [ ] HTTPS termination
  - [ ] HTTP to HTTPS redirect
  - [ ] Security headers

### Success Criteria

- ✅ Full offline installation in under 15 minutes
- ✅ Automatic startup on VM reboot
- ✅ Twilio SMS working in production
- ✅ IT team can deploy without developer assistance
- ✅ Users can log in with credentials
- ✅ HTTPS enforced for all traffic

---

## Phase 3: Enhancements 📋 PLANNED (Jan - Feb 2025)

**Status:** Backlog  
**Goal:** Advanced features for operational flexibility

### Manual Shift Overrides

- [ ] UI for one-time exceptions
  - [ ] Override modal (select date, member, reason)
  - [ ] Visual indicator on calendar for overrides
  - [ ] Audit trail for who made changes
- [ ] API endpoints for overrides
  - [ ] POST /api/v1/schedules/{id}/override
  - [ ] GET /api/v1/schedules/overrides (history)
- [ ] Vacation/swap support
  - [ ] "Request swap" workflow
  - [ ] Approval system (admin or peer)
  - [ ] Email notifications for swaps

### Multi-Level SMS Notifications

- [ ] Enhance SMS to include backup contacts
  - [ ] Primary: On-call member (8:00 AM)
  - [ ] Secondary: Previous in rotation (8:05 AM)
  - [ ] Tertiary: 2 shifts ago (8:10 AM)
- [ ] Role-specific SMS content
  - [ ] Primary: "You are on-call"
  - [ ] Secondary: "You are 1st backup for [name]"
  - [ ] Tertiary: "You are 2nd backup for [name]"
- [ ] Delivery confirmation tracking

### Auto-Regeneration

- [ ] Detect configuration changes
  - [ ] New team member added
  - [ ] Member deactivated
  - [ ] Shift pattern changed
- [ ] Smart regeneration
  - [ ] Only regenerate from change date forward
  - [ ] Preserve past schedules and notifications
  - [ ] Warning banner in UI when schedules out of sync

### Email Backup

- [ ] Email notification system
  - [ ] SMTP configuration
  - [ ] HTML email templates
  - [ ] Send to both SMS + Email
  - [ ] Email-only fallback if SMS fails

### Enhanced Reporting

- [ ] Analytics dashboard
  - [ ] Fair distribution metrics (shifts per member)
  - [ ] Weekend/weekday balance
  - [ ] Notification delivery rates
  - [ ] Response time tracking
- [ ] Exportable reports (CSV, PDF)
  - [ ] Monthly rotation summary
  - [ ] Notification audit log
  - [ ] Fairness report

---

## Phase 4: Advanced Features 💭 FUTURE (3+ months)

**Status:** Vision / Nice-to-Have  
**Goal:** Scale to enterprise multi-team use

### Multi-Team Support

- [ ] Team entity and relationships
- [ ] Team-specific shifts and rotations
- [ ] Cross-team calendar view
- [ ] Separate SMS pools per team

### PostgreSQL Migration

- [ ] Database migration scripts (SQLite → PostgreSQL)
- [ ] Connection pooling for scale
- [ ] Full-text search for notifications
- [ ] Database backups and replication

### Microsoft Teams / Slack Integration

- [ ] Bot notifications in channels
- [ ] Interactive commands (/oncall, /schedule)
- [ ] Inline approvals for swaps
- [ ] Calendar integration

### Mobile Application

- [ ] React Native or Flutter app
- [ ] Push notifications
- [ ] On-call status at a glance
- [ ] Quick swap requests

### Public API

- [ ] REST API for external integrations
- [ ] API key management
- [ ] Rate limiting
- [ ] Webhook support for events

---

## Intentionally Out of Scope

These features are explicitly **NOT** planned:

- ❌ PTO conflict detection (handled manually)
- ❌ Automated incident escalation (use PagerDuty/Opsgenie)
- ❌ Payment/compensation tracking (use HR systems)
- ❌ Self-service shift swapping without approval (requires auth + trust)
- ❌ Voice call notifications (SMS sufficient for MVP)
- ❌ Integration with ticketing systems (out of scope)

---

## Blockers & Risks

### Current Blockers

1. **🔴 Twilio US Number Approval** - Waiting ~1 week, blocks production SMS testing
2. **⚠️ Phone uniqueness constraint disabled** - Must re-enable before production

### Risks

- **Corporate firewall delays** - Offline installer mitigates this
- **IT resource availability** - Comprehensive docs and simple deployment reduce dependency
- **User adoption** - SMS fatigue if too frequent (8am only is good cadence)
- **Twilio costs** - Monitor SMS volume, ~$0.0075/SMS, budget ~$20/month for 7-person team

---

## Success Metrics

### Phase 1 (Achieved ✅)
- ✅ 288 tests passing
- ✅ 85% code coverage
- ✅ 5 functional web pages
- ✅ 0 critical bugs

### Phase 2 (Targets)
- 🎯 < 15 min offline installation
- 🎯 99% SMS delivery rate
- 🎯 0 manual intervention after 1 week
- 🎯 < 2 support tickets from IT

### Phase 3 (Targets)
- 🎯 < 5 min to override a shift
- 🎯 100% backup notification delivery
- 🎯 < 1 scheduling conflict per month

### Phase 4 (Targets)
- 🎯 Support 5+ teams
- 🎯 < 500ms API response times
- 🎯 99.9% uptime
