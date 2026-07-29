# SKILL_REGISTRY.md — Skill 235: beach-cleaning-robot-design

## Skill Registration System

This document defines how skills are registered, resolved, executed, and validated within the beach-cleaning-robot-design harness.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SKILL REGISTRY                               │
├─────────────────────────────────────────────────────────────────┤
│  Registration → Resolution → Execution → Validation             │
└─────────────────────────────────────────────────────────────────┘
        │                    │              │              │
        ▼                    ▼              ▼              ▼
   [Frontmatter]     [Skill Lookup]   [Tool Call]   [Quality Gate]
```

---

## 1. Skill Registration

### Frontmatter Schema

Every skill file (`skills/*.md`) MUST include this frontmatter:

```yaml
---
name: <skill-identifier>           # Unique skill name (kebab-case)
description: <one-line summary>     # When to trigger, what it does
compatibility:                       # Optional: dependencies
  tools: [WebSearch, WebFetch, Read]
  python_version: ">=3.11"
---
```

### Registration Requirements

1. **Name uniqueness**: No duplicate `name` values across all skills
2. **Description pushiness**: Include both what + when to use (make it trigger)
3. **Tool declaration**: List all required tools in compatibility section
4. **File location**: All skills in `skills/` directory with `*.md` extension

### Skill Categories

| Category | Pattern | Example |
|----------|---------|---------|
| Main Harness | `main.md` | `beach-cleaning-robot-design` |
| Sub-Skill | `sub-*.md` | `sub-gather-requirements` |
| Utility | `util-*.md` | `util-format-helper` |

---

## 2. Skill Resolution

### Resolution Algorithm

```
Input: User query / task
Step 1: Extract keywords from query
Step 2: Match against skill descriptions (fuzzy match)
Step 3: Prioritize by: exact match > partial match > category match
Step 4: Return top candidate skill
```

### Resolution JSON Schema

```json
{
  "resolved_skill": {
    "name": "string",
    "path": "string",
    "confidence": "number (0-1)",
    "match_reason": "string"
  }
}
```

---

## 3. Skill Execution

### Execution Flow

```
[PRE-FLIGHT]
  ├─ Language detection (vi/en/other)
  ├─ Input validation against schema
  └─ Tool availability check

[EXECUTION]
  ├─ Load skill instructions
  ├─ Bind tools to execution context
  ├─ Run skill workflow
  └─ Capture outputs

[POST-EXECUTION]
  ├─ Quality gate validation
  ├─ Output formatting
  └─ Result delivery
```

### Execution Context Schema

```json
{
  "execution_context": {
    "skill_name": "string",
    "language": "vi|en",
    "inputs": {},
    "tools_available": ["string"],
    "quality_gates": ["string"],
    "output_format": "structured|freeform"
  }
}
```

---

## 4. Input/Output JSON Schemas

### Requirements Input Schema

```json
{
  "type": "object",
  "properties": {
    "object": {"type": "string", "minLength": 1},
    "scope": {"type": "string"},
    "timeframe": {"type": "string"},
    "available_inputs": {"type": "array"},
    "target_audience": {"type": "string"},
    "language": {"type": "string", "enum": ["vi", "en", "other"]},
    "analysis_type": {"type": "string"}
  },
  "required": ["object"]
}
```

### Evidence Output Schema

```json
{
  "type": "object",
  "properties": {
    "current_data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": {"type": "string"},
          "value": {},
          "timestamp": {"type": "string", "format": "date-time"},
          "tier": {"type": "string", "enum": ["1", "2", "3", "4"]}
        }
      }
    },
    "authoritative_docs": {"type": "array"},
    "recent_news": {"type": "array"},
    "reference_benchmarks": {"type": "array"}
  }
}
```

### Core Analysis Output Schema

```json
{
  "type": "object",
  "properties": {
    "locomotion_collection": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "specification": {},
        "rationale": {"type": "string"}
      }
    },
    "sensing_path_planning": {
      "type": "object",
      "properties": {
        "sensors": {"type": "array"},
        "algorithm": {"type": "string"},
        "tide_aware": {"type": "boolean"}
      }
    },
    "battery_autonomy": {
      "type": "object",
      "properties": {
        "capacity_wh": {"type": "number"},
        "autonomy_hours": {"type": "number"},
        "solar_assist": {"type": "boolean"}
      }
    },
    "reliability": {
      "type": "object",
      "properties": {
        "ip_rating": {"type": "string"},
        "corrosion_protection": {"type": "boolean"},
        "water_ingress_protection": {"type": "boolean"},
        "sand_abrasion_resistance": {"type": "boolean"}
      }
    },
    "scenarios": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "coverage_rate": {"type": "number"}
        }
      }
    }
  },
  "required": ["locomotion_collection", "sensing_path_planning", "battery_autonomy", "reliability", "scenarios"]
}
```

### Final Report Output Schema

```json
{
  "type": "object",
  "properties": {
    "report_metadata": {
      "type": "object",
      "properties": {
        "date": {"type": "string", "format": "date"},
        "analyst": {"type": "string"},
        "language": {"type": "string"},
        "version": {"type": "string"}
      }
    },
    "executive_summary": {"type": "string"},
    "inputs_scope": {"type": "string"},
    "evidence_collected": {"type": "array"},
    "analysis_scorecard": {},
    "action_plan": {"type": "array"},
    "academic_evidence": {"type": "array"},
    "disclosure": {"type": "string"},
    "recommendation": {"type": "string"},
    "quality_gates_passed": {"type": "array"},
    "limitations": {"type": "array"}
  },
  "required": ["report_metadata", "executive_summary", "disclosure", "recommendation"]
}
```

---

## 5. Validation Protocol

### Quality Gate Validation

Each quality gate is validated using this protocol:

```
FOR EACH gate IN quality_gates:
    result = validate(gate, output)
    IF result.passed == FALSE:
        IF result.auto_fix_available:
            output = apply_auto_fix(output, result.fix_instructions)
            result = validate(gate, output)
        IF result.passed == FALSE:
            gate_failure_count += 1
            IF gate_failure_count >= 2:
                emit_limitation_notice(gate)
                CONTINUE to next gate
```

### Validation Result Schema

```json
{
  "type": "object",
  "properties": {
    "gate_name": {"type": "string"},
    "passed": {"type": "boolean"},
    "auto_fix_available": {"type": "boolean"},
    "fix_instructions": {"type": "string"},
    "evidence": {"type": "array"}
  }
}
```

---

## 6. Error Handling & Recovery

### Error Types and Recovery

| Error Type | Detection | Recovery Action | Retry Limit |
|------------|-----------|------------------|-------------|
| Invalid Input | Schema validation fails | Request clarification | 2 |
| Missing Tool | Tool not in available list | Graceful degradation | N/A |
| Source Timeout | No response in 30s | Retry alternate source | 3 |
| Quality Gate Failure | Gate check fails | Auto-fix → Manual flag | 2 |
| Language Detection | Text analysis fails | Default to English | N/A |

### Error Recovery State Machine

```
[OK] → Full execution
[DEGRADED-1] → Some secondary sources used
[DEGRADED-2] → Knowledge base only
[DEGRADED-3] → Missing variables flagged
[FAILED] → Explicit limitation emitted
```

---

## 7. Hooks System

### Available Hooks

| Hook Name | Trigger | Purpose | Parameters |
|-----------|---------|---------|------------|
| `pre-flight` | Before execution | Input validation | `(inputs, context)` |
| `pre-step` | Before each step | State check | `(step_name, state)` |
| `post-step` | After each step | Result capture | `(step_name, result)` |
| `on-error` | On any error | Error handling | `(error, context)` |
| `on-degrade` | On degradation | Flag limitations | `(level, reason)` |
| `post-flight` | After execution | Final validation | `(outputs, context)` |

### Hook Implementation Schema

```json
{
  "hook_name": "string",
  "trigger": "pre-flight|pre-step|post-step|on-error|on-degrade|post-flight",
  "handler": "string",  // Function name or path
  "parameters": {}
}
```

---

## 8. Tool Definitions

### Tool Registry

All tools available to skills are registered in `config/TOOLS.md` with:

- Tool name and description
- Input schema
- Output schema
- Error handling requirements
- Rate limiting (if applicable)

### Tool Call Schema

```json
{
  "tool": "string",
  "parameters": {},
  "timeout_ms": "number",
  "retry_policy": {
    "max_retries": "number",
    "backoff_ms": "number"
  }
}
```

---

## 9. Extensibility Points

### Adding New Skills

1. Create `skills/sub-<name>.md` with proper frontmatter
2. Define input/output schemas in `config/schemas/`
3. Register skill in `config/SKILL_REGISTRY.md`
4. Add test scenarios in `tests/test-scenarios.md`
5. Update quality gates if needed

### Adding New Tools

1. Define tool schema in `config/TOOLS.md`
2. Implement tool handler
3. Add error handling and validation
4. Document in `config/TOOL_REGISTRY.md`

---

## 10. Version Compatibility

| Component | Version | Notes |
|-----------|---------|-------|
| Registry | 2.0.0 | Current |
| Schemas | 2.0.0 | JSON Schema draft-07 |
| Hooks | 1.0.0 | Pre/post execution |
| Tools | 1.0.0 | Stable API |

---

*Last Updated: 2026-07-27*
