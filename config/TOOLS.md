# TOOLS.md — Tool Registry

## Tool Definitions for beach-cleaning-robot-design

All tools available to skills are registered here with schemas and execution handlers.

---

## 1. WebSearch Tool

### Purpose
Search the web for current Beach-Cleaning Robotics & Coastal Engineering information.

### Schema
```json
{
  "tool": "WebSearch",
  "description": "Search web for domain-relevant information",
  "input_schema": {
    "query": {"type": "string", "minLength": 2},
    "max_results": {"type": "number", "default": 10, "maximum": 50},
    "recency_filter": {"type": "string", "enum": ["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"]}
  },
  "output_schema": {
    "results": {
      "type": "array",
      "items": {
        "title": {"type": "string"},
        "url": {"type": "string"},
        "snippet": {"type": "string"},
        "source": {"type": "string"},
        "date": {"type": "string"}
      }
    }
  },
  "timeout_ms": 30000,
  "retry_policy": {"max_retries": 2, "backoff_ms": 1000}
}
```

### Error Handling
- Timeout: Return cached results if available, else empty array
- No results: Return empty array with flag
- Rate limit: Exponential backoff up to 5 seconds

---

## 2. WebFetch Tool

### Purpose
Fetch content from specific URLs for detailed analysis.

### Schema
```json
{
  "tool": "WebFetch",
  "description": "Fetch content from a specific URL",
  "input_schema": {
    "url": {"type": "string", "format": "uri"},
    "prompt": {"type": "string"},
    "timeout_seconds": {"type": "number", "default": 30, "maximum": 120}
  },
  "output_schema": {
    "content": {"type": "string"},
    "metadata": {
      "title": {"type": "string"},
      "source": {"type": "string"},
      "fetched_at": {"type": "string", "format": "date-time"}
    }
  },
  "timeout_ms": 45000,
  "retry_policy": {"max_retries": 3, "backoff_ms": 2000}
}
```

### Error Handling
- 404/403: Flag as unavailable, suggest alternative
- Timeout: Retry with longer timeout
- Parse error: Return raw content with parsing flag

---

## 3. Read Tool

### Purpose
Read files from the local filesystem, primarily SECOND-KNOWLEDGE-BRAIN.md.

### Schema
```json
{
  "tool": "Read",
  "description": "Read local files",
  "input_schema": {
    "file_path": {"type": "string"},
    "offset": {"type": "number", "default": 0},
    "limit": {"type": "number", "default": 2000}
  },
  "output_schema": {
    "content": {"type": "string"},
    "lines_read": {"type": "number"},
    "total_lines": {"type": "number"},
    "encoding": {"type": "string"}
  },
  "timeout_ms": 5000,
  "retry_policy": {"max_retries": 1, "backoff_ms": 500}
}
```

### Error Handling
- File not found: Return error with suggested paths
- Encoding error: Try UTF-8 fallback encodings
- Permission denied: Flag and suggest alternative

---

## 4. Write Tool

### Purpose
Write content to files, primarily for knowledge base updates.

### Schema
```json
{
  "tool": "Write",
  "description": "Write content to local files",
  "input_schema": {
    "file_path": {"type": "string"},
    "content": {"type": "string"},
    "mode": {"type": "string", "enum": ["overwrite", "append"], "default": "overwrite"}
  },
  "output_schema": {
    "bytes_written": {"type": "number"},
    "file_path": {"type": "string"},
    "success": {"type": "boolean"}
  },
  "timeout_ms": 10000,
  "retry_policy": {"max_retries": 2, "backoff_ms": 1000}
}
```

### Error Handling
- Path not found: Create directory structure
- Permission denied: Flag and suggest alternative location
- Disk full: Emit critical error

---

## 5. Bash Tool

### Purpose
Execute shell commands, primarily for knowledge_updater.py.

### Schema
```json
{
  "tool": "Bash",
  "description": "Execute shell commands",
  "input_schema": {
    "command": {"type": "string"},
    "timeout": {"type": "number", "default": 120000, "maximum": 600000},
    "working_directory": {"type": "string"}
  },
  "output_schema": {
    "stdout": {"type": "string"},
    "stderr": {"type": "string"},
    "exit_code": {"type": "number"},
    "duration_ms": {"type": "number"}
  },
  "timeout_ms": 120000,
  "retry_policy": {"max_retries": 1, "backoff_ms": 1000}
}
```

### Error Handling
- Command not found: Suggest installation path
- Timeout: Kill process and flag
- Non-zero exit: Return stderr with analysis

---

## 6. Skill Tool

### Purpose
Invoke sub-skills within the harness.

### Schema
```json
{
  "tool": "Skill",
  "description": "Invoke sub-skills",
  "input_schema": {
    "skill": {"type": "string"},
    "args": {"type": "string"}
  },
  "output_schema": {
    "result": {"type": "string"},
    "skill_name": {"type": "string"},
    "execution_time_ms": {"type": "number"},
    "quality_gates_passed": {"type": "array"}
  },
  "timeout_ms": 60000,
  "retry_policy": {"max_retries": 1, "backoff_ms": 2000}
}
```

### Error Handling
- Skill not found: Check registry, suggest alternatives
- Quality gate failure: Return partial results with flags
- Timeout: Return partial results with timeout flag

---

## Tool Priority Matrix

| Tool | Priority | Fallback | Notes |
|------|----------|----------|-------|
| Read | High | None | Required |
| Skill | High | None | Core to harness |
| WebSearch | Medium | Knowledge base | Degraded mode |
| WebFetch | Medium | Cached version | Degraded mode |
| Write | Low | Queue for later | Non-critical |
| Bash | Low | Manual execution | Non-critical |

---

## Rate Limiting

| Tool | Rate Limit | Window |
|------|------------|--------|
| WebSearch | 10 requests | 1 minute |
| WebFetch | 20 requests | 1 minute |
| Read | No limit | N/A |
| Write | No limit | N/A |
| Bash | 5 requests | 1 minute |
| Skill | No limit | N/A |

---

## Tool Health Monitoring

### Health Checks
- Availability: Tool responds within timeout
- Accuracy: Output matches expected schema
- Rate limiting: Respects defined limits

### Health Status Schema
```json
{
  "tool_name": {"type": "string"},
  "status": {"type": "string", "enum": ["healthy", "degraded", "down"]},
  "last_check": {"type": "string", "format": "date-time"},
  "response_time_ms": {"type": "number"},
  "error_rate": {"type": "number"}
}
```

---

*Last Updated: 2026-07-27*
