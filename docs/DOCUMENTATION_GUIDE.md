# Documentation Guide

This guide defines the purpose and update strategy for each documentation file in WhoseOnFirst.

## Documentation Hierarchy

```
LINEAR (Active Work Management)
  ↓ references
/docs/planning/PRD.md (Living Requirements Document)
  ↓ informs
CLAUDE.md (AI Context - Root Directory)
  ↓ generates
CHANGELOG.md (Version History)
  ↓ summarizes
README.md (User-Facing Overview)
```

## File Purposes & Update Strategy

### 1. Linear Issues (Primary Source of Truth)

**Purpose:** Active work tracking and sprint planning

**Location:** https://linear.app/hextrackr (Team: WhoseOnFirst)

**Contains:**
- Current sprint tasks and backlog
- Bug reports and feature requests
- Issue status (Todo → In Progress → Done)
- Implementation notes and discussion

**Update When:**
- Starting new work
- Completing features
- Finding bugs
- Planning next sprint

**Labels to Use:**
- Type: `Feature`, `Bug`, `Enhancement`, `Documentation`
- Domain: `backend`, `frontend`, `scheduler`, `docker`, `database`, `testing`
- Phase: `phase-1`, `phase-2`, `phase-3`, `phase-4`

**Issue Format:**
```
Title: Clear, descriptive (e.g., "Schedule Auto-Renewal Feature")
Description: 
- Problem statement
- Implementation approach
- Files modified
- Testing notes
Git Branch: Auto-generated from title
```

---

### 2. PRD.md (Living Requirements Document)

**Purpose:** Authoritative requirements specification that evolves with the product

**Location:** `/docs/planning/PRD.md`

**Contains:**
- Numbered functional requirements (REQ-001, REQ-002, etc.)
- Non-functional requirements (performance, security, etc.)
- User stories and use cases
- Success metrics
- Out-of-scope items

**Update When:**
- Adding new features (create new REQ-XXX)
- Completing requirements (mark with ✅)
- Changing scope or priorities
- Quarterly reviews

**Format for New Requirements:**
```markdown
### REQ-XXX: [Feature Name] (Linear: WHO-X)
**Status:** ✅ Complete / 🔄 In Progress / 📋 Planned
**Priority:** High / Medium / Low
**Phase:** 1 / 2 / 3 / 4

**Description:** [What the requirement is]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Implementation Notes:** Brief technical approach
**Related Issues:** WHO-X, WHO-Y
```

**Review Schedule:**
- Weekly: Mark completed requirements
- Monthly: Add new planned requirements
- Quarterly: Full document review and cleanup

---

### 3. CLAUDE.md (AI Context File)

**Purpose:** Authoritative context for Claude Code CLI sessions - orient AI within 30 seconds

**Location:** `/CLAUDE.md` (root directory - required by Claude Code)

**Contains:**
- Quick start overview (30-second read)
- Documentation hierarchy explanation
- Current project status and next steps
- Docker-first development workflow
- MCP tools usage patterns
- Critical implementation details (brief)
- Security and testing requirements
- Links to detailed documentation

**Update When:**
- Completing major phases (Phase 1 → Phase 2)
- Changing development workflow (e.g., Docker adoption)
- Adding new critical patterns
- Quarterly architecture reviews

**Keep It Lean:**
- Target: ~10KB (~2,000 lines)
- Detailed code examples → `/docs/reference/code-patterns.md`
- Full architecture → `/docs/planning/architecture.md`
- Complete requirements → `/docs/planning/PRD.md`

**Update Frequency:**
- After major milestones: Always
- Minor features: Rarely
- Bug fixes: Never (unless workflow changes)

---

### 4. CHANGELOG.md (Version History)

**Purpose:** Release notes and version history for users and developers

**Location:** `/CHANGELOG.md` (root directory)

**Contains:**
- Version-specific changes (Added, Changed, Fixed, Removed)
- Docker rebuild requirements
- Breaking changes
- Migration notes
- Release dates

**Update When:**
- Creating releases (v1.0.0, v1.1.0, etc.)
- Immediately after tagging a release
- Never for unreleased work (use [Unreleased] section)

**Format:**
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Group changes: Added, Changed, Deprecated, Removed, Fixed, Security
- Include Linear issue references: `(WHO-X)`
- Note Docker rebuild requirements

**Generation Strategy:**
```bash
# At release time:
1. Review completed Linear issues since last release
2. Group by category (Added, Changed, Fixed)
3. Write user-facing descriptions (not technical details)
4. Add Docker rebuild notes if needed
5. Update version number and date
6. Commit with message: "docs: release v1.X.X"
```

---

### 5. README.md (User-Facing Overview)

**Purpose:** First impression for users and contributors - getting started guide

**Location:** `/README.md` (root directory)

**Contains:**
- Project overview (what it does)
- Key features (bullet list)
- Current version badge
- Quick start instructions
- Technology stack summary
- Project roadmap (high-level phases)
- Links to documentation
- Links to Linear issue tracker

**Update When:**
- Major feature releases (v1.0, v2.0)
- Changing quick start steps
- Updating deployment instructions
- Changing technology stack

**Keep It High-Level:**
- Link to `/docs/planning/` for detailed architecture
- Link to Linear for issue tracking
- Link to CHANGELOG.md for version history
- Don't duplicate content from other docs

**Update Frequency:**
- Major releases: Always
- Minor releases: Rarely (unless user-facing changes)
- Patches: Never

---

### 6. Reference Documentation (Code Examples)

**Purpose:** Detailed code patterns and examples for developers

**Location:** `/docs/reference/code-patterns.md`

**Contains:**
- Repository pattern examples
- Service layer examples
- APScheduler configuration
- Twilio integration examples
- Database migration patterns
- Test fixture examples

**Update When:**
- Establishing new patterns
- Changing architectural approaches
- Adding complex integrations

**Referenced By:**
- CLAUDE.md (links to specific sections)
- PRD.md (links to implementation examples)

---

### 7. Planning Documentation (Deep Dives)

**Purpose:** Comprehensive planning and architectural documentation

**Location:** `/docs/planning/`

**Files:**
- `architecture.md` - System design, data flow, component details
- `technical-stack.md` - Technology decisions with rationale
- `research-notes.md` - Technology evaluation and trade-offs
- `PRD.md` - Product requirements (living document)

**Update When:**
- Making architectural decisions
- Changing technology stack
- Adding new integrations
- Quarterly reviews

**Keep Updated:**
- Architecture diagrams
- Database schema (reflect actual migrations)
- Technology versions
- Decision rationale

---

### 8. Archive (Historical Snapshots)

**Purpose:** Preserve historical documentation for reference

**Location:** `/docs/archive/`

**When to Archive:**
- Planning documents after phase completion
- Status reports after milestone releases
- Old roadmaps after major pivots
- Outdated architecture documents

**Naming Convention:**
```
MVP_STATUS-v0.2.0-20251108.md
ROADMAP-PHASE1-20251104.md
ARCHITECTURE-LEGACY-20251101.md
```

**Never Archive:**
- Current CLAUDE.md
- Current PRD.md
- Current README.md
- Active planning docs

---

## Documentation Workflow

### Starting a New Feature

1. **Create Linear issue** with descriptive title and acceptance criteria
2. **Check PRD.md** - Does this need a new REQ-XXX? Add it.
3. **Start work** - Claude Code reads CLAUDE.md for context
4. **Reference patterns** - Check `/docs/reference/code-patterns.md` for examples

### Completing a Feature

1. **Update Linear issue** to Done with implementation notes
2. **Mark PRD requirement** as ✅ Complete
3. **Add to CHANGELOG.md** [Unreleased] section
4. **Consider CLAUDE.md** - Does workflow change? (rare)

### Creating a Release

1. **Review Linear** - Gather all Done issues since last release
2. **Update CHANGELOG.md** - Move [Unreleased] to versioned section
3. **Update README.md** - Update version badge and features if needed
4. **Tag release** - `git tag v1.X.X`
5. **Verify CLAUDE.md** - Update "Current Status" section

### Quarterly Review

1. **Review PRD.md** - Mark completed, add planned, remove obsolete
2. **Review CLAUDE.md** - Update current phase and critical patterns
3. **Review architecture.md** - Ensure database schema matches reality
4. **Archive old docs** - Move outdated snapshots to `/docs/archive/`

---

## AI Session Best Practices

### For Claude Desktop (Strategic Planning)

**Read First:**
1. Linear issues (active work)
2. PRD.md (requirements context)
3. CLAUDE.md (project orientation)

**Update:**
- Linear issues (create new, update status)
- PRD.md (add new requirements)
- Planning documents (architecture decisions)

### For Claude Code CLI (Implementation)

**Read First:**
1. CLAUDE.md (30-second orientation)
2. Assigned Linear issue
3. `/docs/reference/code-patterns.md` (implementation patterns)

**Update:**
- Code files
- Test files
- Linear issue status
- CHANGELOG.md [Unreleased] section

**Use MCP Tools:**
```bash
# Before reading files manually:
1. memento semantic_search - Find past decisions
2. claude-context search_code - Find exact locations
3. Read only the specific files identified
```

---

## Documentation Anti-Patterns (Avoid These)

❌ **Duplicating information** across multiple files
✅ Single source of truth with links

❌ **Updating CHANGELOG.md** for unreleased work
✅ Wait until release, then generate from Linear issues

❌ **Detailed code examples** in CLAUDE.md
✅ Keep CLAUDE.md lean, link to `/docs/reference/`

❌ **Frozen PRD** after Phase 1
✅ Living document that evolves with product

❌ **Stale status reports** in `/docs/`
✅ Archive old snapshots with dates

❌ **Manual file reading** without MCP tools
✅ Use semantic search first (80% token savings)

❌ **Technical details** in README.md
✅ High-level overview with links to detailed docs

---

## Quick Reference Card

| File | Purpose | Update Frequency | Audience |
|------|---------|------------------|----------|
| **Linear** | Active work | Daily | Team |
| **PRD.md** | Requirements | Weekly | Product/Dev |
| **CLAUDE.md** | AI context | Per phase | AI agents |
| **CHANGELOG.md** | Release notes | Per release | Users/Devs |
| **README.md** | Overview | Major releases | Users |
| **code-patterns.md** | Examples | Per pattern | Developers |
| **architecture.md** | Design | Quarterly | Architects |

---

## Questions?

If you're unsure which file to update:
1. **Is it active work?** → Linear issue
2. **Is it a new requirement?** → PRD.md
3. **Is it changing workflow?** → CLAUDE.md
4. **Is it a release?** → CHANGELOG.md
5. **Is it a code pattern?** → code-patterns.md
6. **Is it architectural?** → architecture.md

**Last Updated:** 2025-11-10
**Version:** 1.0.0
