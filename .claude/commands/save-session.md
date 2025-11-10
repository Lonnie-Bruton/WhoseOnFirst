---
description: Save WhoseOnFirst session + auto-extract insights to Memento
allowed-tools: mcp__memento__create_entities, mcp__memento__create_relations, mcp__memento__add_observations
argument-hint: [keyword]
---
Save complete WhoseOnFirst session context + insights to Memento: $ARGUMENTS

**Action**: Comprehensive knowledge capture with auto-generated session ID.

**Project**: Auto-detects "WHOSEONFIRST" from current directory

**Usage**:
```bash
/save-session
/save-session keyword:auto-renewal
/save-session keyword:docker-workflow
```

**Auto-Generated Session ID Format**:
```
WHOSEONFIRST-{KEYWORD}-{YYYYMMDD}-{HHMMSS}

Examples:
- WHOSEONFIRST-AUTORENEWAL-20251109-120000
- WHOSEONFIRST-DOCKER-20251109-143000
- WHOSEONFIRST-LINEARSETUP-20251109-150000
```

**Two-Phase Process**:

### Phase 1: Extract Insights (if quality threshold met)

Save insights that meet ANY of:
- ✅ Breakthrough discovery or novel solution
- ✅ Reusable pattern applicable to other projects
- ✅ Best practice or anti-pattern identified
- ✅ Workflow optimization with measurable impact
- ✅ Docker-specific workflow improvements

**Example Insight**:
```javascript
mcp__memento__create_entities([{
  name: "Insight: Docker-First Development Workflow",
  entityType: "WHOSEONFIRST:WORKFLOW:PATTERN",
  observations: [
    "TIMESTAMP: 2025-11-09T18:00:00.000Z",
    "ABSTRACT: Docker rebuild checkpoints for Python code changes",
    "SUMMARY: WhoseOnFirst requires Docker container rebuild after any Python code changes...",
    "INSIGHT_ID: WHOSEONFIRST-INSIGHT-20251109-180000"
  ]
}])
```

**Insight Tags**:
```javascript
mcp__memento__add_observations({
  observations: [{
    entityName: "Insight: Docker-First Development Workflow",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: workflow",
      "TAG: pattern",
      "TAG: docker",
      "TAG: reusable",
      "TAG: week-45-2025"
    ]
  }]
})
```

### Phase 2: Save Session Context (always)

**Session Entity**:
```javascript
mcp__memento__create_entities([{
  name: "Session: WHOSEONFIRST-AUTORENEWAL-20251109-120000",
  entityType: "WHOSEONFIRST:DEVELOPMENT:SESSION",
  observations: [
    "TIMESTAMP: 2025-11-09T12:00:00.000Z",
    "ABSTRACT: Auto-renewal feature implementation",
    "SUMMARY: Implemented schedule auto-renewal system with Settings model...",
    "SESSION_ID: WHOSEONFIRST-AUTORENEWAL-20251109-120000",
    "OUTCOME: Settings table added with migration",
    "OUTCOME: Scheduler job registered at 2:00 AM",
    "OUTCOME: Frontend toggle integrated",
    "DECISION: Use database-backed configuration instead of env variables",
    "PATTERN: Docker rebuild after each batch of Python changes"
  ]
}])
```

**Session Tags**:
```javascript
mcp__memento__add_observations({
  observations: [{
    entityName: "Session: WHOSEONFIRST-AUTORENEWAL-20251109-120000",
    contents: [
      "TAG: project:whoseonfirst",
      "TAG: linear:WHO-2",
      "TAG: backend",
      "TAG: feature",
      "TAG: completed",
      "TAG: week-45-2025",
      "TAG: v1.0.0" // if applicable
    ]
  }]
})
```

**Output**:
```
✅ Session saved successfully!
📋 Session ID: WHOSEONFIRST-AUTORENEWAL-20251109-120000

💡 Extracted 2 insights:
  1. Docker-First Development Workflow
  2. Settings Service Pattern with Typed Values

🔗 2 SESSION→INSIGHT relations created

🔍 Recall commands:
  Session: /recall-conversation id:WHOSEONFIRST-AUTORENEWAL-20251109-120000
  Insights: Search Memento for "docker workflow" or "settings pattern"
```

**Tag Reference**: See `/docs/TAXONOMY.md` for full tag system
