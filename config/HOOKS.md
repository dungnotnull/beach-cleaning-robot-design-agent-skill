# HOOKS.md — Hooks System Documentation

## Production-Grade Hooks for beach-cleaning-robot-design

Lifecycle hooks for state synchronization, event emission, and graceful error handling.

---

## Hook System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXECUTION FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [pre-flight] → [Step 1] → [post-step] → [Step 2] → ... →     │
│       ↓             ↓              ↓                              │
│   [on-error]   [on-degrade]  [post-flight]                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hook Definitions

### 1. pre-flight Hook

**Trigger:** Before any skill execution begins

**Purpose:** Input validation and preparation

**Parameters:**
```typescript
interface PreFlightParams {
  inputs: Record<string, unknown>;
  context: ExecutionContext;
  skill_name: string;
}
```

**Returns:**
```typescript
interface PreFlightResult {
  valid: boolean;
  errors?: string[];
  normalized_inputs?: Record<string, unknown>;
  warnings?: string[];
}
```

**Implementation:**
- Validate input against JSON schema
- Detect language (vi/en/other)
- Check tool availability
- Normalize data formats

**Error Handling:**
- Invalid input: Return errors and request clarification
- Missing tools: Degrade gracefully
- Language detection failure: Default to English

---

### 2. pre-step Hook

**Trigger:** Before each step in the workflow

**Purpose:** State verification and preparation

**Parameters:**
```typescript
interface PreStepParams {
  step_name: string;
  step_number: number;
  state: WorkflowState;
  inputs: Record<string, unknown>;
}
```

**Returns:**
```typescript
interface PreStepResult {
  ready: boolean;
  errors?: string[];
  prepared_inputs?: Record<string, unknown>;
}
```

**Implementation:**
- Verify required state exists
- Check dependencies from previous steps
- Prepare step-specific inputs
- Log step start

**Error Handling:**
- Missing state: Request re-run from previous step
- Invalid inputs: Normalize or request clarification

---

### 3. post-step Hook

**Trigger:** After each step completes

**Purpose:** Result capture and state update

**Parameters:**
```typescript
interface PostStepParams {
  step_name: string;
  step_number: number;
  result: StepResult;
  state: WorkflowState;
}
```

**Returns:**
```typescript
interface PostStepResult {
  state_updated: boolean;
  quality_gate_passed: boolean;
  errors?: string[];
  next_step_ready: boolean;
}
```

**Implementation:**
- Validate step output against schema
- Update workflow state
- Run step-specific quality gates
- Log step completion

**Error Handling:**
- Invalid output: Request retry or degradation
- Quality gate failure: Attempt auto-fix
- State conflict: Merge strategies

---

### 4. on-error Hook

**Trigger:** When any error occurs during execution

**Purpose:** Centralized error handling and recovery

**Parameters:**
```typescript
interface OnErrorParams {
  error: Error;
  context: ExecutionContext;
  step_name?: string;
  severity: "low" | "medium" | "high" | "critical";
}
```

**Returns:**
```typescript
interface OnErrorResult {
  action: "retry" | "degrade" | "abort" | "ignore";
  retry_after_ms?: number;
  degradation_level?: number;
  user_message?: string;
}
```

**Implementation:**
- Classify error type and severity
- Determine recovery action
- Prepare user-facing message
- Log error with context

**Error Types:**
- **Network errors:** Retry with exponential backoff
- **Validation errors:** Request clarification
- **Timeout errors:** Degrade or use cached data
- **Critical errors:** Abort with explicit notice

---

### 5. on-degrade Hook

**Trigger:** When degradation level increases

**Purpose:** Flag limitations and adjust output

**Parameters:**
```typescript
interface OnDegradeParams {
  from_level: number;
  to_level: number;
  reason: string;
  context: ExecutionContext;
}
```

**Returns:**
```typescript
interface OnDegradeResult {
  limitation_emitted: boolean;
  output_adjusted: boolean;
  alternative_suggested?: string;
}
```

**Implementation:**
- Log degradation with reason
- Emit limitation banner
- Adjust output expectations
- Suggest alternatives if available

**Degradation Levels:**
- **Level 0:** Full operation
- **Level 1:** Some secondary sources used
- **Level 2:** Knowledge base only
- **Level 3:** Missing variables flagged
- **Level 4:** All sources failed

---

### 6. post-flight Hook

**Trigger:** After all execution completes

**Purpose:** Final validation and delivery preparation

**Parameters:**
```typescript
interface PostFlightParams {
  outputs: Record<string, unknown>;
  context: ExecutionContext;
  execution_time_ms: number;
  quality_gates_results: QualityGateResult[];
}
```

**Returns:**
```typescript
interface PostFlightResult {
  delivery_ready: boolean;
  final_quality_check: boolean;
  formatted_output?: string;
  metadata?: Record<string, unknown>;
}
```

**Implementation:**
- Run final quality gate validation
- Format output according to template
- Add metadata (timestamp, version, etc.)
- Prepare for delivery

**Error Handling:**
- Quality gate failure: Run auto-fix or emit limitation
- Format error: Return raw output with flag
- Metadata error: Use minimal metadata

---

## Hook Execution Order

```
1. pre-flight (skill start)
   └─► on-error (if validation fails)

2. For each step:
   a. pre-step
   b. [execute step]
   c. post-step
      └─► on-degrade (if quality degradation)

3. post-flight (skill end)
   └─► on-error (if final validation fails)
```

---

## Hook Configuration

### Hook Registration

```json
{
  "hook_name": "pre-flight",
  "enabled": true,
  "priority": 1,
  "handler": "scripts/hooks.py::pre_flight_handler",
  "parameters": {
    "strict_validation": true,
    "language_detection": true
  }
}
```

### Hook State Schema

```typescript
interface HookState {
  execution_id: string;
  start_time: Date;
  current_step?: string;
  degradation_level: number;
  errors: ErrorRecord[];
  warnings: WarningRecord[];
  quality_gates_passed: string[];
  quality_gates_failed: string[];
}
```

---

## Event Emission

### Event Types

| Event | Trigger | Payload |
|-------|---------|---------|
| `skill.started` | pre-flight complete | `{skill_name, inputs}` |
| `step.started` | pre-step complete | `{step_name, step_number}` |
| `step.completed` | post-step complete | `{step_name, result}` |
| `error.occurred` | on-error | `{error, severity, recovery}` |
| `degradation.changed` | on-degrade | `{from_level, to_level, reason}` |
| `skill.completed` | post-flight complete | `{outputs, duration_ms}` |

### Event Schema

```typescript
interface SkillEvent {
  event_type: string;
  timestamp: Date;
  execution_id: string;
  payload: Record<string, unknown>;
}
```

---

## Error Recovery Strategies

### Retry Strategy

```typescript
interface RetryStrategy {
  max_retries: number;
  initial_delay_ms: number;
  max_delay_ms: number;
  exponential_backoff: boolean;
  jitter: boolean;
}
```

### Degradation Strategy

```typescript
interface DegradationStrategy {
  level_0: "full";
  level_1: "secondary_sources";
  level_2: "knowledge_base_only";
  level_3: "flag_missing";
  level_4: "emit_unavailable";
}
```

---

## Hook Performance Monitoring

### Metrics to Track

- Hook execution time (percentiles: p50, p95, p99)
- Hook failure rate
- Error recovery success rate
- Degradation frequency by level

### Monitoring Schema

```typescript
interface HookMetrics {
  hook_name: string;
  execution_count: number;
  success_count: number;
  failure_count: number;
  avg_duration_ms: number;
  p95_duration_ms: number;
  error_types: Record<string, number>;
}
```

---

## Best Practices

1. **Keep hooks lightweight** - Don't block execution
2. **Log everything** - Maintain audit trail
3. **Fail gracefully** - Never crash the harness
4. **User transparency** - Emit clear messages
5. **State consistency** - Maintain valid state at all times

---

## Hook Testing

### Test Scenarios

1. **pre-flight:** Invalid inputs, missing tools, language detection
2. **pre-step:** Missing state, invalid dependencies
3. **post-step:** Invalid output, quality gate failure
4. **on-error:** Network errors, timeouts, validation failures
5. **on-degrade:** All degradation levels
6. **post-flight:** Quality gate failures, format errors

### Test Framework

```bash
python scripts/test_hooks.py --coverage --verbose
```

---

*Last Updated: 2026-07-27*
