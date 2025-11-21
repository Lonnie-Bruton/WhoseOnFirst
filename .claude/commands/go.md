---
description: Quick startup - run prime and prepare for work
---

# WhoseOnFirst Go - Quick Session Startup

**Purpose**: Execute `/prime` context loading and prepare for development work.

---

## EXECUTION SEQUENCE

### Step 1: Run Prime Context Loading

Execute the prime command to gather all context:

```
/prime
```

**This will**:
- Refresh git context and codebase index
- Query Linear for active issues
- Search Memento for insights
- Verify code locations
- Save prime log to `/docs/prime/YYYY-MM-DD-HHMMSS.md`

**Wait for prime to complete before proceeding.**

---

### Step 2: Summarize Readiness

After prime completes, provide a brief CLI summary:

```markdown
## 🚀 WhoseOnFirst Session Ready

**Active Work**:
- [WHO-XX]: [Title] → Next: [specific action at file:line]
- [WHO-XX]: [Title] → Blocked: [reason]

**Recent Context**:
- [count] commits since last session
- [count] Memento insights found
- Index: ✅ [X files, Y chunks]

**Ready to Code**: ✅ Yes / ⚠️ [blocker noted]

**Saved**: `/docs/prime/YYYY-MM-DD-HHMMSS.md`
```

---

### Step 3: Offer Next Actions

Based on Linear In Progress issues, suggest immediate actions:

```markdown
**Suggested Commands**:

1. **Continue [WHO-XX]**:
   - Read: `src/[file].py:[line]`
   - Pattern: [reference similar code]
   - Action: [specific implementation step]

2. **Start [WHO-XX]**:
   - Verify: Search for "[keyword]" in codebase
   - Plan: [high-level approach]
   - Begin: [entry point file:line]

**Or**: Ask me "What should I work on?" for guided selection
```

---

### Step 4: Optional Memento Save

If prime discovered important new patterns or the Linear issues have significant context, offer to save to Memento:

**Ask user**: "Would you like me to save today's prime context to Memento for future sessions?"

If yes, create entities:
```javascript
mcp__memento__create_entities({
  entities: [{
    name: "WHOSEONFIRST-Prime-YYYY-MM-DD-HHMMSS",
    entityType: "WHOSEONFIRST:DEVELOPMENT:SESSION",
    observations: [
      "Prime log executed at [timestamp]",
      "Active issues: [WHO-XX], [WHO-YY] - [brief descriptions]",
      "Recent completions: [WHO-ZZ] - [impact]",
      "Code verified: [key file locations]",
      "Next actions: [specific file:line references]"
    ]
  }]
})
```

**Tags to add**:
- `project:whoseonfirst`
- `session:prime-YYYY-MM-DD`
- `week-[XX]-2025`
- `linear:WHO-XX` (for each active issue)
- `status:in-progress`

---

## SUCCESS CRITERIA

Go is complete when:

1. ✅ Prime log saved to `/docs/prime/`
2. ✅ Active issues summarized with file:line references
3. ✅ Next actions clearly identified
4. ✅ Codebase index confirmed ready
5. ✅ User knows exactly what to work on next

---

## TYPICAL EXECUTION TIME

- Prime execution: 1-2 minutes
- Summary + suggestions: 30 seconds
- Optional Memento save: 30 seconds

**Total**: ~2-3 minutes to full context and readiness

---

**Go Version**: 1.0.0 (WhoseOnFirst-specific)
**Last Updated**: 2025-11-21
