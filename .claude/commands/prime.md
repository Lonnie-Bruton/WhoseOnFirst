---
description: Load WhoseOnFirst context - verify code, check Linear, search insights
allowed-tools: Read, Bash, Write, mcp__memento__*, mcp__linear-server__*, mcp__claude-context__*
---

# WhoseOnFirst Prime - Streamlined Session Context

**Purpose**: Load essential context through verification-first workflow. Saves to `/docs/prime/` for session history.

**Project**: WhoseOnFirst (Automated on-call rotation system)

---

## EXECUTION SEQUENCE

Follow phases in order. Each phase takes 15-30 seconds.

### Phase 1: Git Context + Codebase Index (REQUIRED)

Execute these commands:

1. **Current timestamp**: `date "+%Y-%m-%d %H:%M:%S %Z"`
2. **Recent commits**: `git log --oneline -5` (last 5 commits)
3. **Uncommitted changes**: `git status --short`
4. **Current branch**: `git branch --show-current`

5. **Re-index codebase** (always refresh at session start):
   ```javascript
   mcp__claude-context__index_codebase({
     path: "/Volumes/DATA/GitHub/WhoseOnFirst",
     splitter: "ast",
     force: false  // Use true if major changes or search issues
   })
   ```

6. **Check indexing status**:
   ```javascript
   mcp__claude-context__get_indexing_status({
     path: "/Volumes/DATA/GitHub/WhoseOnFirst"
   })
   ```

**Wait for indexing to complete before proceeding to Phase 4**

---

### Phase 2: Linear Active Work (REQUIRED)

Query Linear to understand current priorities:

**Team Name**: "WhoseOnFirst" (no -Dev suffix)

1. **In Progress issues**:
   ```javascript
   mcp__linear-server__list_issues({
     team: "WhoseOnFirst",
     state: "In Progress",
     includeArchived: false
   })
   ```

2. **For each In Progress issue**, get full details:
   ```javascript
   mcp__linear-server__get_issue({ id: "[issue-id]" })
   ```
   Extract: Description, labels, linked PRD requirements, technical keywords

3. **Todo issues** (next up):
   ```javascript
   mcp__linear-server__list_issues({
     team: "WhoseOnFirst",
     state: "Todo",
     includeArchived: false,
     limit: 5
   })
   ```

4. **Recent completions** (last 7 days):
   ```javascript
   mcp__linear-server__list_issues({
     team: "WhoseOnFirst",
     state: "Done",
     updatedAt: "-P7D",
     includeArchived: false,
     limit: 5
   })
   ```

**Compile keywords** from Linear issues:
- Feature names (e.g., "escalation contacts", "dual-device SMS")
- Component names (e.g., "TeamMemberService", "notification_service")
- File paths mentioned in descriptions

---

### Phase 3: Memento Insights Search (REQUIRED)

Search for past session learnings and manual insights:

**Current week calculation**: Extract week number from Phase 1 timestamp (e.g., week-47-2025)

1. **Recent session insights**:
   ```javascript
   mcp__memento__semantic_search({
     query: "WHOSEONFIRST session insight week-[CURRENT_WEEK]-2025 completed pattern lesson",
     limit: 10,
     min_similarity: 0.4,
     hybrid_search: true
   })
   ```

2. **Project-specific patterns** (use Linear keywords from Phase 2):
   ```javascript
   mcp__memento__semantic_search({
     query: "whoseonfirst [LINEAR_KEYWORDS] rotation scheduler twilio fastapi docker",
     limit: 8,
     min_similarity: 0.4,
     hybrid_search: false
   })
   ```

**Tag patterns to note**:
- `project:whoseonfirst`
- `linear:WHO-X`
- Status: `completed`, `in-progress`, `pattern`, `lesson-learned`
- Temporal: `week-XX-2025`, `v1.X.X`

---

### Phase 4: Code Verification (REQUIRED)

**Wait for Phase 1 indexing to complete before running these searches**

Verify codebase structure using keywords from Phases 2 & 3:

**All searches use**:
- path: `/Volumes/DATA/GitHub/WhoseOnFirst`
- limit: 5

1. **Architecture verification**:
   ```javascript
   mcp__claude-context__search_code({
     query: "FastAPI routes services repositories dependency injection",
     limit: 5
   })
   ```

2. **Recent features** (from git commits + Linear):
   ```javascript
   mcp__claude-context__search_code({
     query: "[GIT_FEATURES] [LINEAR_FEATURES] implementation",
     limit: 5
   })
   ```
   Example: "escalation contacts dual-device SMS notification implementation"

3. **Core systems verification**:
   ```javascript
   mcp__claude-context__search_code({
     query: "rotation algorithm APScheduler notification_service Twilio",
     limit: 5
   })
   ```

**Record key file locations** with line numbers for next actions.

---

### Phase 5: Documentation Check (REQUIRED)

Read essential docs to understand current state:

1. **Read CHANGELOG.md** (root):
   - Extract current version
   - Note recent changes
   - Identify version drift if any

2. **Read PRD.md** (living requirements):
   ```
   /docs/planning/PRD.md
   ```
   - Focus on "Current Status" section
   - Note active requirements
   - Check for blockers

3. **Check Docker status**:
   ```bash
   docker ps --filter "name=whoseonfirst" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
   ```

---

### Phase 6: Save Prime Log (REQUIRED)

Create timestamped log in `/docs/prime/`:

**Filename**: `YYYY-MM-DD-HHMMSS.md` (from Phase 1 timestamp)

**Template**:

```markdown
# WhoseOnFirst Prime Log
**Timestamp**: YYYY-MM-DD HH:MM:SS TZ
**Branch**: [from git]
**Version**: [from CHANGELOG.md]
**Index Status**: ✅ [X files, Y chunks] or ⏳ In Progress

---

## 📋 Git Context

**Recent Commits** (last 5):
1. [hash] [message]
2. [hash] [message]
...

**Uncommitted Changes**: [Yes/No - count if yes]

**Current Branch**: [branch name]

---

## 🎯 Linear Active Work

### In Progress ([count] issues)

**[WHO-XX]: [Title]**
- **Description**: [Brief summary]
- **Labels**: [list]
- **Files Mentioned**: [file:line references if any]
- **Next Action**: [specific task]

### Todo ([count] issues)

- **[WHO-XX]**: [Title] - [one-line description]

### Recent Completions (last 7 days)

- **[WHO-XX]**: [Title] (completed [date])

**Keywords Extracted**: [list 5-8 keywords for searches]

---

## 🧠 Memento Insights

**Query Tags**: `project:whoseonfirst`, `week-[XX]-2025`

**Key Insights Found** ([count] entities):

1. **[Entity Name]**: [Key observation or pattern]
2. **[Entity Name]**: [Key observation or pattern]

**Relevant Patterns**: [any architectural or workflow patterns discovered]

---

## 🔍 Code Verification

**Index Status**: [Completion %, file count, chunk count]

### Architecture Points

- **Services Layer**: `src/services/[file].py:[line]`
- **API Routes**: `src/api/v1/[file].py:[line]`
- **Repositories**: `src/repositories/[file].py:[line]`

### Recent Feature Locations

- **[Feature Name]**: `file.py:line` - [brief description]

### Core Systems

- **Rotation Algorithm**: `src/services/schedule_service.py:[line]`
- **Scheduler**: `src/scheduler/scheduler.py:[line]`
- **Notifications**: `src/services/notification_service.py:[line]`

---

## 📊 Technical Baseline

**Runtime Environment**:
- Python: [version from Dockerfile or requirements]
- Database: SQLite at `./data/whoseonfirst.db`
- Docker: [dev/prod container status]
- Port: [8900 dev / 8000 prod]

**Docker Status**:
```
[output from docker ps]
```

**Documentation Status**:
- CHANGELOG.md: [version]
- PRD.md: [current phase]
- CLAUDE.md: [last updated date]

---

## 📝 Next Actions

Based on Linear In Progress issues:

1. **[WHO-XX]**: [Specific action] at `file.py:line`
   - Pattern: [reference to similar code]
   - Dependencies: [any blockers]

2. **[WHO-XX]**: [Specific action] at `file.py:line`

3. **Other**: [Any non-tracked maintenance or improvements]

---

## 💡 Session Context Summary

[2-3 paragraphs summarizing:
- Current project state and active work
- Recent progress and completions
- Technical patterns or insights discovered
- Any blockers or concerns noted
- Readiness to begin work]

---

**Context Loading Complete** ✅
**Estimated Session Duration**: [based on Linear issues]
**Ready to Code**: [Yes/No - note any blockers]
```

---

## SUCCESS CRITERIA

Prime is complete when you can answer:

1. ✅ What Linear issues are in progress?
2. ✅ What code was changed in last 5 commits?
3. ✅ Where is the [feature] implemented? (file:line)
4. ✅ What patterns did we learn in recent sessions?
5. ✅ Is the codebase indexed and searchable?
6. ✅ What's the next action with specific file location?

---

## NOTES

- **Duration**: 1-2 minutes typical
- **Index**: Always refresh at session start (Phase 1)
- **Linear Team**: "WhoseOnFirst" (exact match)
- **Memento Tags**: Use `project:whoseonfirst` filter
- **Verification First**: Never guess file locations—use claude-context search
- **Save Locally**: `/docs/prime/` for easy grep/search later

---

**Prime Version**: 1.0.0 (WhoseOnFirst-specific)
**Last Updated**: 2025-11-21
