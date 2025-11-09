# WhoseOnFirst Memento Knowledge Graph Taxonomy

> **Purpose:** Defines tagging conventions and entity structure for WhoseOnFirst project in Memento MCP  
> **Last Updated:** 2025-11-09  
> **Version:** 1.0.0

---

## Entity Naming Convention

### Classification Pattern: PROJECT:DOMAIN:TYPE

**PROJECT** (First Level):
- `WHOSEONFIRST` - All entities must use this project prefix

**DOMAIN** (Second Level):
- `BACKEND` - API, services, repositories, database
- `FRONTEND` - UI pages, JavaScript, HTML/CSS
- `DEPLOYMENT` - Docker, Podman, RHEL, installation
- `TESTING` - Test suites, coverage, QA
- `DOCUMENTATION` - Docs, guides, planning
- `ARCHITECTURE` - System design, decisions

**TYPE** (Third Level):
- `SESSION` - Work sessions and progress updates
- `HANDOFF` - Session transition packages
- `DECISION` - Architectural or technical choices
- `INSIGHT` - Learned patterns or breakthroughs
- `ISSUE` - Problems, bugs, blockers
- `MILESTONE` - Phase completions, major achievements

### Examples:
- `Session: WHOSEONFIRST-PLANNING-20251109-DOCKERPREP`
- `Decision: WHOSEONFIRST-PODMAN-OVER-K8S`
- `Milestone: WHOSEONFIRST-PHASE1-MVP-COMPLETE`
- `Handoff: WHOSEONFIRST-FRONTEND-TO-BACKEND-INTEGRATION`

---

## Tag Taxonomy

### 1. Project Tag (Required)
Every entity MUST have this tag:
- `project:whoseonfirst`

### 2. Phase Tags
Track project phases:
- `phase-1` - MVP (Complete)
- `phase-2` - Deployment & Auth (In Progress)
- `phase-3` - Enhancements (Planned)
- `phase-4` - Advanced Features (Future)

### 3. Domain Tags
Functional area classification:
- `backend` - FastAPI, services, repositories, database
- `frontend` - HTML, CSS, JavaScript, Tabler UI
- `deployment` - Docker, Podman, RHEL, containerization
- `testing` - Unit tests, integration tests, pytest
- `documentation` - Docs, guides, planning documents
- `architecture` - System design, technical decisions

### 4. Technology Tags
Specific technologies:
- `fastapi` - FastAPI framework
- `twilio` - SMS integration
- `apscheduler` - Background scheduling
- `sqlalchemy` - Database ORM
- `docker` - Containerization
- `podman` - RHEL container runtime
- `rhel` - Red Hat Enterprise Linux
- `pytest` - Testing framework
- `tabler` - Frontend UI framework

### 5. Feature Tags
Specific features:
- `rotation-algorithm` - On-call rotation logic
- `sms-notifications` - Twilio SMS delivery
- `shift-templates` - Shift configuration
- `schedule-generation` - Schedule creation
- `rotation-order` - Drag-drop ordering
- `escalation-chain` - Backup contact system
- `offline-install` - Air-gapped deployment

### 6. Workflow Tags
Status tracking:
- `completed` - Finished work
- `in-progress` - Active development
- `blocked` - Waiting on dependencies
- `needs-review` - Requires validation
- `planning` - Design phase
- `archived` - Historical reference

### 7. Impact Tags
Change significance:
- `breaking-change` - Backwards incompatible
- `critical` - System-breaking or urgent
- `enhancement` - Improvement to existing feature
- `feature` - New functionality
- `bugfix` - Defect correction
- `security` - Security-related change

### 8. Learning Tags
Knowledge capture:
- `lesson-learned` - Mistake or learning experience
- `pattern` - Reusable solution
- `breakthrough` - Major discovery
- `pain-point` - Identified problem area
- `best-practice` - Recommended approach
- `anti-pattern` - What not to do
- `reusable` - Applicable to other projects

### 9. Temporal Tags
Time-based markers:
- `week-XX-2025` - Week number (e.g., `week-45-2025`)
- `q4-2024` - Quarter tracking
- `nov-2024` - Month markers
- `v0.1.0` - Version tags

### 10. Context Tags
Deployment environment:
- `local-dev` - Development on Mac
- `proxmox-lab` - Testing on Proxmox RHEL VM
- `production` - Corporate RHEL VM deployment

---

## Required Observations (In Order)

Every entity MUST include these observations:

1. **TIMESTAMP:** ISO 8601 format (e.g., `2025-11-09T19:30:00.000Z`)
2. **ABSTRACT:** One-line summary (< 100 chars)
3. **SUMMARY:** Detailed description (comprehensive context)
4. **[TYPE]_ID:** Unique identifier
   - `SESSION_ID: WHOSEONFIRST-[FEATURE]-[DATE]-[TIME]`
   - `DECISION_ID: WHOSEONFIRST-[DECISION]-[DATE]`
   - `HANDOFF_ID: WHOSEONFIRST-[FROM]-TO-[TO]-[DATE]`
   - `MILESTONE_ID: WHOSEONFIRST-[PHASE]-[NAME]-[DATE]`

---

## Tagging Examples

### Session Entity
```javascript
// Create entity
mcp__memento__create_entities([{
  name: "Session: WHOSEONFIRST-DOCKER-20251109-140000",
  entityType: "WHOSEONFIRST:DEPLOYMENT:SESSION",
  observations: [
    "TIMESTAMP: 2025-11-09T14:00:00.000Z",
    "ABSTRACT: Docker containerization and offline installer planning",
    "SUMMARY: Planned Docker/Podman deployment strategy...",
    "SESSION_ID: WHOSEONFIRST-DOCKER-20251109-140000"
  ]
}]);

// Add tags
mcp__memento__add_observations({
  observations: [{
    entityName: "Session: WHOSEONFIRST-DOCKER-20251109-140000",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: phase-2",
      "TAG: deployment",
      "TAG: docker",
      "TAG: podman",
      "TAG: rhel",
      "TAG: offline-install",
      "TAG: planning",
      "TAG: week-45-2025"
    ]
  }]
});
```

### Decision Entity
```javascript
mcp__memento__add_observations({
  observations: [{
    entityName: "Decision: WHOSEONFIRST-PODMAN-OVER-K8S",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: phase-2",
      "TAG: deployment",
      "TAG: architecture",
      "TAG: podman",
      "TAG: docker",
      "TAG: rhel",
      "TAG: decision",
      "TAG: completed",
      "TAG: best-practice",
      "TAG: reusable"
    ]
  }]
});
```

### Handoff Entity
```javascript
mcp__memento__add_observations({
  observations: [{
    entityName: "Handoff: WHOSEONFIRST-BACKEND-TO-FRONTEND",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: phase-1",
      "TAG: backend",
      "TAG: frontend",
      "TAG: handoff",
      "TAG: completed",
      "TAG: week-44-2025"
    ]
  }]
});
```

### Milestone Entity
```javascript
mcp__memento__add_observations({
  observations: [{
    entityName: "Milestone: WHOSEONFIRST-PHASE1-MVP-COMPLETE",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: phase-1",
      "TAG: milestone",
      "TAG: completed",
      "TAG: breakthrough",
      "TAG: week-45-2025"
    ]
  }]
});
```

---

## Search Strategies

### Use `semantic_search` for:
- Conceptual queries: "how did we implement SMS retry logic?"
- Thematic searches: "deployment decisions in Phase 2"
- Discovery: "similar challenges we solved before"
- Cross-cutting concerns: "security considerations across all phases"

### Use `search_nodes` for:
- Exact tag matching: `"project:whoseonfirst phase-2 docker"`
- Specific IDs: `"SESSION_ID: WHOSEONFIRST-DOCKER-20251109-140000"`
- Status queries: `"in-progress deployment"`
- Time-based: `"week-45-2025 completed"`

---

## Query Patterns

### Find Work by Phase
```
"phase-1 completed" - All Phase 1 work
"phase-2 in-progress" - Current Phase 2 tasks
"phase-3 planning" - Planned Phase 3 features
```

### Find Technical Decisions
```
"decision architecture" - All architecture decisions
"deployment docker podman" - Container decisions
"backend fastapi rotation-algorithm" - Backend tech choices
```

### Find Lessons Learned
```
"lesson-learned twilio" - SMS integration learnings
"pain-point deployment" - Deployment challenges
"breakthrough testing" - Testing insights
```

### Time-Based Queries
```
"week-45-2025 project:whoseonfirst" - This week's work
"nov-2024 milestone" - November milestones
"q4-2024 completed" - Q4 completions
```

---

## Maintenance Rules

### Weekly Cleanup
1. Review and consolidate similar tags
2. Update temporal tags (week numbers)
3. Archive completed sessions older than 30 days

### Entity Retention
- Keep all DECISION and MILESTONE entities permanently
- Keep HANDOFF entities for 90 days
- Keep SESSION entities for 30 days (unless tagged `archived`)
- Never delete entities tagged `lesson-learned` or `breakthrough`

---

## Integration with Documentation

Memento complements (not replaces) these files:
- **CLAUDE.md** - AI assistant context (authoritative reference)
- **ROADMAP.md** - Phase tracking and planning
- **CURRENT-SPRINT.md** - Active task list
- **CHANGELOG.md** - Version history and changes

Use memento for:
- "Why did we make this decision?"
- "What challenges did we face with Twilio?"
- "How did we solve the rotation order problem?"
- "What's the history of the offline installer idea?"

Use documentation for:
- "How do I deploy this?"
- "What endpoints exist?"
- "What's the current status?"
- "What tasks are next?"

---

## Quick Reference

### Must-Have Tags
- [ ] `project:whoseonfirst`
- [ ] Phase tag (`phase-1`, `phase-2`, etc.)
- [ ] Domain tag (`backend`, `frontend`, `deployment`, etc.)
- [ ] Temporal tag (`week-XX-2025`)

### Search Decision Tree
1. **Looking for why/how?** → `semantic_search`
2. **Looking for specific tag/ID?** → `search_nodes`
3. **Exploring related ideas?** → `semantic_search` with `min_similarity: 0.5`
4. **Finding recent work?** → `search_nodes` with temporal tags

---

*Authority: WhoseOnFirst Development Workflow*  
*Adapted from: HexTrackr Taxonomy v1.2.0*
