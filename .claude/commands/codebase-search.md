---
description: Search WhoseOnFirst codebase using natural language queries
allowed-tools: mcp__claude-context__search_code
---
Search the WhoseOnFirst codebase with semantic queries: $ARGUMENTS

**Action**: Use claude-context to find code by natural language description.

**Usage**:
```bash
/codebase-search rotation algorithm circular shift
/codebase-search schedule generation database query
/codebase-search twilio sms notification sending
/codebase-search apscheduler job registration
```

**Tool**:
```javascript
mcp__claude-context__search_code({
  path: "/Volumes/DATA/GitHub/WhoseOnFirst",
  query: "$ARGUMENTS",
  limit: 10,
  extensionFilter: [] // optional: [".py", ".js", ".html"]
})
```

**Returns**:
- Relevant code snippets with file:line numbers
- Top 10 most semantically similar code blocks
- Exact locations to Read tool for detailed inspection

**Best Practices**:
- Use descriptive queries: "schedule generation rotation algorithm"
- Include technical terms: "APScheduler job registration"
- Combine concepts: "Twilio SMS send retry logic"
- Filter by extension if needed: extensionFilter: [".py"]

**Token Savings**: 80-90% vs. manually reading files
