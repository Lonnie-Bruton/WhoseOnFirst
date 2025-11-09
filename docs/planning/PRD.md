# Product Requirements Document (PRD)
## WhoseOnFirst - On-Call Team SMS Notifier

**Version:** 1.0  
**Date:** November 4, 2025  
**Status:** Planning Phase  
**Author:** Development Team

---

## Executive Summary

WhoseOnFirst is an automated on-call rotation and SMS notification system designed to manage fair scheduling for technical teams. The system ensures equitable shift distribution using a simple circular rotation algorithm, schedules the double-shift during the workweek (Tue-Wed) to minimize weekend impact, and automatically notifies on-call personnel at shift start times.

---

## Problem Statement

### Current Pain Points
- Manual on-call rotation management is error-prone and time-consuming
- No automated notification system for shift changes
- Difficulty ensuring fair rotation across team members
- Challenge in preventing individuals from being on-call multiple weekend days consecutively
- Need for flexible shift patterns (24-hour and 48-hour shifts)
- Team size fluctuations require dynamic schedule adjustments

### Target Users
- **Primary:** IT/DevOps teams of 5-10 members requiring on-call coverage
- **Secondary:** Team leads and managers who manage on-call schedules
- **Future:** Organizations with multiple teams requiring coordinated coverage

---

## Goals and Objectives

### Primary Goals
1. Automate daily SMS notifications to on-call personnel at 8:00 AM CST
2. Implement fair rotation algorithm ensuring no weekend-day clustering
3. Provide simple administrative interface for schedule management
4. Support flexible shift patterns (24-hour and 48-hour durations)
5. Enable easy addition/removal of team members

### Success Metrics
- 100% on-time notification delivery (8:00 AM CST ±1 minute)
- Zero instances of unfair weekend distribution
- <5 minutes required for administrative tasks
- 99.9% system uptime during business hours
- Successful deployment within 90 days

---

## User Stories

### As an On-Call Team Member
- I want to receive an SMS at 8:00 AM CST when my shift starts
- I want to know exactly when my shift ends
- I want fair weekend distribution so I'm not on-call multiple weekend days
- I want visibility into the upcoming schedule

### As a Team Administrator
- I want to easily add/remove team members from rotation
- I want to customize shift patterns (days and durations)
- I want to manually override the schedule when needed
- I want to see a history of notifications sent
- I want to ensure fair rotation across all team members

### As a Manager
- I want confidence that coverage is maintained 24/7
- I want audit logs of all schedule changes
- I want to see notification delivery status
- I want minimal maintenance overhead

---

## Functional Requirements

### Core Features (MVP - Phase 1)

#### 1. Team Member Management
- **REQ-001:** System shall store team member information (name, phone number, active status)
- **REQ-002:** System shall support adding new team members
- **REQ-003:** System shall support removing/deactivating team members
- **REQ-004:** System shall validate phone numbers for E.164 format
- **REQ-005:** System shall prevent duplicate phone numbers

#### 2. Shift Configuration
- **REQ-006:** System shall support configurable shift patterns
- **REQ-007:** System shall support 24-hour shift durations
- **REQ-008:** System shall support 48-hour shift durations
- **REQ-009:** System shall assign shifts to days of the week
- **REQ-010:** System shall number shifts sequentially (Shift 1, Shift 2, etc.)

#### 3. Schedule Generation
- **REQ-011:** System shall implement fair circular rotation algorithm
- **REQ-012:** System shall distribute on-call burden fairly via double-shift (48h) during workweek (Tue-Wed)
- **REQ-013:** System shall rotate shift assignments weekly (each member moves to next shift)
- **REQ-014:** System shall generate schedules at least 4 weeks in advance
- **REQ-015:** System shall recalculate schedules when team composition changes

#### 4. SMS Notifications
- **REQ-016:** System shall send SMS notifications at 8:00 AM CST daily
- **REQ-017:** SMS message shall include: shift start time, duration, and on-call person's name
- **REQ-018:** System shall use Twilio API for SMS delivery
- **REQ-019:** System shall log all SMS attempts (success/failure)
- **REQ-020:** System shall retry failed SMS notifications up to 3 times

#### 5. Administrative Interface
- **REQ-021:** System shall provide web-based admin dashboard
- **REQ-022:** Dashboard shall display current week's schedule
- **REQ-023:** Dashboard shall show upcoming 4 weeks of assignments
- **REQ-024:** Dashboard shall allow manual schedule overrides
- **REQ-025:** Dashboard shall display notification history

### Future Features (Post-MVP)

#### Phase 2 - Enhanced Administration
- **REQ-026:** Multi-user authentication system
- **REQ-027:** Role-based access control (Admin, Viewer)
- **REQ-028:** Team member self-service portal
- **REQ-029:** Shift swap functionality
- **REQ-030:** Email notifications as backup to SMS

#### Phase 3 - Integrations
- **REQ-031:** Microsoft Teams integration
- **REQ-032:** Slack integration
- **REQ-033:** Calendar export (iCal format)
- **REQ-034:** REST API for external integrations
- **REQ-035:** Webhook support for schedule changes

#### Phase 4 - Advanced Features
- **REQ-036:** Support for multiple teams
- **REQ-037:** PTO/vacation management and manual shift overrides
  - UI to select a future date/shift and manually assign a different team member
  - Override applies to single occurrence only (doesn't affect rotation)
  - Visual indicator in calendar for overridden shifts
- **REQ-038:** Multi-level SMS notifications with escalation chain
  - Send 3 SMS messages per shift start (Primary, Secondary, Tertiary)
  - Primary: "You are PRIMARY on-call. Backup: [Name]. Escalation: [Name]"
  - Secondary: "You are BACKUP on-call. Primary: [Name]. Escalation: [Name]"
  - Tertiary: "You are ESCALATION on-call. Primary: [Name]. Backup: [Name]"
  - Uses rotation_order-based backup calculation (already implemented in frontend)
- **REQ-039:** Automatic schedule regeneration on configuration changes
  - Auto-regenerate when team members added/removed/reordered
  - Auto-regenerate when shifts added/modified/deleted
  - Warning banner if changes detected but schedule not regenerated
  - Option to manually trigger regeneration vs. auto-regeneration setting
- **REQ-040:** Analytics and reporting dashboard
- **REQ-041:** Mobile application

---

## Non-Functional Requirements

### Performance
- **NFR-001:** SMS notifications shall be sent within 60 seconds of scheduled time
- **NFR-002:** Web dashboard shall load in <2 seconds
- **NFR-003:** API responses shall complete in <500ms (95th percentile)
- **NFR-004:** System shall support up to 20 team members without performance degradation

### Reliability
- **NFR-005:** System shall maintain 99.9% uptime during business hours (8 AM - 8 PM CST)
- **NFR-006:** System shall persist all data reliably
- **NFR-007:** System shall recover automatically from transient failures
- **NFR-008:** Scheduler shall resume after system restart without missing notifications

### Security
- **NFR-009:** System shall store sensitive credentials in environment variables
- **NFR-010:** System shall use HTTPS for all web traffic
- **NFR-011:** System shall sanitize all user inputs to prevent injection attacks
- **NFR-012:** Phone numbers shall be stored securely and not exposed in logs

### Scalability
- **NFR-013:** System shall support migration from SQLite to PostgreSQL
- **NFR-014:** Architecture shall support horizontal scaling in future
- **NFR-015:** Database schema shall support multi-tenant architecture

### Maintainability
- **NFR-016:** Code shall maintain >80% test coverage
- **NFR-017:** System shall provide comprehensive logging
- **NFR-018:** Configuration shall be externalized (no hard-coded values)
- **NFR-019:** System shall use modern Python best practices (type hints, async/await)

### Usability
- **NFR-020:** Admin interface shall be intuitive and require no training
- **NFR-021:** SMS messages shall be clear and concise (<160 characters preferred)
- **NFR-022:** Error messages shall be actionable and user-friendly

---

## Technical Constraints

### Infrastructure
- **CONSTRAINT-001:** Must run on RHEL 10
- **CONSTRAINT-002:** Must support Docker containerization
- **CONSTRAINT-003:** Must operate in air-gapped environment (no internet for production VM, except Twilio API)
- **CONSTRAINT-004:** Must use approved SMS provider (Twilio)

### Technology Stack
- **CONSTRAINT-005:** Backend must use Python 3.11+
- **CONSTRAINT-006:** Must use FastAPI framework
- **CONSTRAINT-007:** Must support SQLite for initial deployment
- **CONSTRAINT-008:** Must support PostgreSQL migration path

### Development
- **CONSTRAINT-009:** Development environment: macOS with Docker Desktop
- **CONSTRAINT-010:** Testing environment: Proxmox home lab
- **CONSTRAINT-011:** Version control: Git/GitHub
- **CONSTRAINT-012:** Primary development tool: Claude-Code CLI

---

## Use Case: Typical Weekly Rotation

### Example Team Configuration
**Team Members:** Bob, Dave, Steve, John, Paul, Matt, Sam (7 members)

**Shift Pattern:**
- Shift 1: Monday (24 hours, 8am-8am)
- Shift 2: Tuesday-Wednesday (48 hours, 8am-8am)
- Shift 3: Thursday (24 hours, 8am-8am)
- Shift 4: Friday (24 hours, 8am-8am)
- Shift 5: Saturday (24 hours, 8am-8am)
- Shift 6: Sunday (24 hours, 8am-8am)

### Week 1 Assignments
| Shift | Day(s) | Duration | Assigned To |
|-------|--------|----------|-------------|
| 1 | Monday | 24h | Bob |
| 2 | Tue-Wed | 48h | Dave |
| 3 | Thursday | 24h | Steve |
| 4 | Friday | 24h | John |
| 5 | Saturday | 24h | Paul |
| 6 | Sunday | 24h | Matt |

*Note: Sam rotates in during Week 2*

### Week 2 Assignments (Rotation)
| Shift | Day(s) | Duration | Assigned To |
|-------|--------|----------|-------------|
| 1 | Monday | 24h | Sam |
| 2 | Tue-Wed | 48h | Bob |
| 3 | Thursday | 24h | Dave |
| 4 | Friday | 24h | Steve |
| 5 | Saturday | 24h | John |
| 6 | Sunday | 24h | Paul |

### Fairness Algorithm (Circular Rotation)
- Each week, assignments rotate: person on Shift N moves to Shift N+1
- Simple circular rotation: `member_index = (shift_index + week_offset) % team_size`
- Person on Shift 6 wraps back to Shift 1 the following week
- **No special weekend logic needed**: The 48-hour double shift (Tue-Wed) naturally distributes workload fairly
- With 7 team members and 6 shifts, one person is "off" each week, rotating through the team
- Over multiple weeks, every member gets equal distribution of all shifts including the double shift

---

## Sample SMS Messages

### Standard Shift Start Notification
```
WhoseOnFirst: Your on-call shift has started.
Duration: 24 hours (until 8:00 AM tomorrow)
Questions? Contact admin at [number]
```

### Multi-Day Shift Notification
```
WhoseOnFirst: Your on-call shift has started.
Duration: 48 hours (until 8:00 AM Thursday)
Questions? Contact admin at [number]
```

---

## Out of Scope (V1)

The following features are explicitly out of scope for the initial release:
- Mobile applications (iOS/Android)
- Voice call notifications
- Integration with ticketing systems
- Automated incident escalation
- On-call payment/compensation tracking
- Multi-team coordination
- Advanced reporting and analytics
- Self-service shift swapping
- PTO/vacation conflict detection

---

## Dependencies

### External Services
- Twilio API (SMS provider)
- RHEL 10 VM (production environment)

### Internal Dependencies
- None - self-contained application

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Twilio API outage | High | Low | Log failures, implement retry logic, manual backup process |
| Schedule algorithm bug | High | Medium | Comprehensive unit tests, manual override capability |
| SMS delivery failures | Medium | Medium | Retry logic, notification logs, admin alerts |
| Database corruption | High | Low | Daily backups, SQLite journal mode |
| Timezone handling errors | Medium | Medium | Use pytz/zoneinfo, extensive testing |
| Team member churn | Low | High | Simple onboarding/offboarding UI |

---

## Timeline and Phases

### Phase 1: MVP Development (Weeks 1-6)
- Week 1-2: Core backend (database, models, API)
- Week 2-3: Scheduler and SMS integration
- Week 3-4: Admin frontend interface
- Week 4-6: Testing, Docker deployment, documentation

### Phase 2: Enhancement (Weeks 7-10)
- Multi-user authentication
- Enhanced UI/UX
- Additional notification channels
- Performance optimization

### Phase 3: Integration (Weeks 11-14)
- Microsoft Teams integration
- REST API for external consumers
- Advanced reporting

### Phase 4: Scale (Weeks 15+)
- Multi-team support
- PostgreSQL migration
- Mobile app development

---

## Approval and Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | [TBD] | | |
| Tech Lead | [TBD] | | |
| Stakeholder | [TBD] | | |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-04 | Development Team | Initial PRD creation |

---

## Appendix

### Glossary
- **On-Call:** State of being available to respond to incidents during designated time period
- **Shift:** Defined time period for on-call coverage
- **Rotation:** Pattern of shift assignments across team members
- **Fair Distribution:** Algorithm ensuring equitable assignment of shifts, especially weekends

### References
- [Twilio SMS API Documentation](https://www.twilio.com/docs/sms)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
