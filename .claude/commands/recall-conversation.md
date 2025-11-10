---
description: Recall a specific WhoseOnFirst conversation by session ID from Memento
allowed-tools: mcp__memento__search_nodes, mcp__memento__semantic_search, mcp__memento__open_nodes
argument-hint: id:SESSION_ID or keyword:KEYWORD
---
Recall a WhoseOnFirst conversation by session ID: $ARGUMENTS

**Action**: Retrieve a previously saved conversation using its unique session ID.

**Project**: Auto-detects "WHOSEONFIRST" from current directory

**Usage**:
```bash
/recall-conversation id:WHOSEONFIRST-AUTORENEWAL-20251109-120000
/recall-conversation id:WHO-2
/recall-conversation keyword:auto-renewal
/recall-conversation keyword:docker workflow
```

**Search by ID** (exact match using search_nodes):
```javascript
mcp__memento__search_nodes({
  query: "SESSION_ID: WHOSEONFIRST-AUTORENEWAL-20251109-120000"
})
```

**Search by Keyword** (conceptual using semantic_search):
```javascript
mcp__memento__semantic_search({
  query: "auto-renewal schedule configuration",
  limit: 10,
  min_similarity: 0.6,
  hybrid_search: true
})
```

**Search by Tags** (exact tags using search_nodes):
- `"project:whoseonfirst spec:001"` - Specific spec work
- `"linear:WHO-2 completed"` - Completed Linear issue
- `"week-45-2025 backend"` - This week's backend work

**Output Format**:
```
📋 Session ID: WHOSEONFIRST-AUTORENEWAL-20251109-120000
📅 Date: 2025-11-09
🎯 Topic: Schedule Auto-Renewal Feature Implementation
🔍 Key Outcomes:
  - Created Settings model for auto-renewal configuration
  - Implemented daily scheduler job at 2:00 AM CST
  - Added frontend toggle UI in schedule.html
  - Resolved Docker rebuild workflow

💡 Context: Completed auto-renewal feature allowing automatic
schedule extension when running low on future schedules.
```

**Tag Reference**: See `/docs/TAXONOMY.md` for full tag system
