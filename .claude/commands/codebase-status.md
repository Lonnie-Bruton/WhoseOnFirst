---
description: Check WhoseOnFirst codebase indexing status
allowed-tools: mcp__claude-context__get_indexing_status, mcp__claude-context__clear_index
---
Check the indexing status of the WhoseOnFirst codebase.

**Action**: Verify if codebase is indexed and show progress.

**Status Check**:
```javascript
mcp__claude-context__get_indexing_status({
  path: "/Volumes/DATA/GitHub/WhoseOnFirst"
})
```

**Returns**:
- Whether codebase is indexed
- Indexing progress (if in progress)
- Last update timestamp
- Completion percentage

**Clear Index** (if needed):
```javascript
mcp__claude-context__clear_index({
  path: "/Volumes/DATA/GitHub/WhoseOnFirst"
})
```

**When to Clear**:
- Before force reindex
- If index is corrupted
- When switching to different splitter method
- Troubleshooting search issues
