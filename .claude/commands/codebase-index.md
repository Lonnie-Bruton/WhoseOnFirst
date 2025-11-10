---
description: Index WhoseOnFirst codebase for semantic search capabilities
allowed-tools: mcp__claude-context__index_codebase
---
Use the **claude-context** MCP server to index the WhoseOnFirst codebase:

```javascript
mcp__claude-context__index_codebase({
  path: "/Volumes/DATA/GitHub/WhoseOnFirst",
  splitter: "ast",
  force: true
})
```

**Parameters**:
- `path`: Absolute path to WhoseOnFirst codebase
- `splitter`: "ast" for syntax-aware code splitting (recommended for Python/JavaScript)
- `force`: true to reindex if already indexed (use when code has changed significantly)

**When to Reindex**:
- After major code changes (new features, refactoring)
- When search results seem outdated
- After adding new files or modules
- First time setting up WhoseOnFirst development

**Estimated Time**: 30-60 seconds for WhoseOnFirst codebase
