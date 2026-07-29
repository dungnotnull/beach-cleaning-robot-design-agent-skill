# CLAUDE.md — Skill 235: beach-cleaning-robot-design v2.0.0

## Skill Identity
- **Skill Name:** `beach-cleaning-robot-design`
- **Tagline:** Beach-Cleaning Robot Design (Path Optimization vs Current) — Beach-Cleaning Robotics & Coastal Engineering analysis & decision-support harness.
- **Current Phase:** Phase 5 — Production Ready v2.0.0
- **Version:** 2.0.0
- **Folder:** `D:\972026\235-beach-cleaning-robot-design\`

---

## Problem This Skill Solves

This skill provides a structured, evidence-backed analytical workflow for **Beach-Cleaning Robotics & Coastal Engineering**. It combines:

- Real-time data aggregation from authoritative sources
- Recognized domain methods and frameworks
- Academic research integration
- Production-grade error handling
- Structured logging and monitoring
- Self-improving knowledge pipeline

---

## v2.0.0 Architecture

### Enhanced Modular Structure

```
beach-cleaning-robot-design/
├── config/              # Configuration & schemas
│   ├── SKILL_REGISTRY.md         # Skill registration system
│   ├── TOOLS.md                  # Tool definitions
│   ├── HOOKS.md                  # Hooks system documentation
│   └── schemas/                  # JSON schemas
│       ├── requirements-input.schema.json
│       ├── evidence-output.schema.json
│       ├── core-analysis-output.schema.json
│       └── final-report-output.schema.json
├── scripts/             # Production-grade utilities
│   ├── hooks.py                  # Lifecycle hooks implementation
│   ├── schema_validator.py       # JSON schema validation
│   └── logger.py                 # Structured logging system
├── references/          # Domain reference documentation
│   └── domain-methods.md         # Beach-Cleaning Robotics methods
├── assets/              # Templates & static resources
│   └── templates/
│       ├── report-template-en.md
│       └── report-template-vi.md
├── skills/              # Harness and sub-skills
│   ├── main.md                  # Main orchestrator
│   ├── sub-gather-requirements.md
│   ├── sub-evidence-collector.md
│   ├── sub-core-analysis.md
│   ├── sub-knowledge-updater.md
│   └── sub-advisor.md
├── tools/               # Knowledge pipeline
│   ├── knowledge_updater.py      # v1.0 (legacy)
│   ├── knowledge_updater_v2.py   # v2.0 (production-grade)
│   ├── test_knowledge_updater.py
│   └── run_test_scenarios.py
├── tests/               # Comprehensive testing
│   ├── test-scenarios.md
│   ├── test-scenarios_v2.md
│   ├── test_hooks.py
│   └── test_schema_validator.py
├── logs/                # Structured logs (generated)
│   ├── hooks.log
│   ├── knowledge_updater.log
│   ├── knowledge_updater.jsonl
│   └── knowledge_updater_metrics.json
└── SECOND-KNOWLEDGE-BRAIN.md     # Self-improving knowledge base
```

---

## Harness Flow Summary

```
USER INPUT
    │
    ▼
[main.md — beach-cleaning-robot-design v2.0]
    │
    ├─► [PRE-FLIGHT HOOK]
    │   ├─ Language detection (vi/en)
    │   ├─ Input validation (JSON schema)
    │   ├─ Tool availability check
    │   └─ State initialization
    │
    ├─► Step 1: sub-gather-requirements
    │   └─► [PRE-STEP HOOK] → [POST-STEP HOOK]
    │
    ├─► Step 2: sub-evidence-collector
    │   └─► [PRE-STEP HOOK] → [POST-STEP HOOK]
    │       ├─ WebSearch/WebFetch with retry
    │       ├─ Fallback to knowledge base
    │       └─ [ON-DEGRADE HOOK] if sources fail
    │
    ├─► Step 3: sub-core-analysis
    │   └─► [PRE-STEP HOOK] → [POST-STEP HOOK]
    │       └─ Domain methods applied
    │
    ├─► Step 4: sub-knowledge-updater
    │   └─► [PRE-STEP HOOK] → [POST-STEP HOOK]
    │       └─ Knowledge base queried
    │
    ├─► Step 5: sub-advisor
    │   └─► [PRE-STEP HOOK] → [POST-STEP HOOK]
    │       └─ Synthesis with disclosure
    │
    ├─► [POST-FLIGHT HOOK]
    │   ├─ Quality gate validation
    │   ├─ Output formatting (template)
    │   ├─ Metadata attachment
    │   └─ Delivery preparation
    │
    └─► OUTPUT DELIVERY
        ├─ Structured report (EN/VI)
        ├─ Quality gate checklist
        ├─ Execution metrics
        └─ Limitation notices (if degraded)
```

---

## Quality Gates (v2.0 Enhanced)

### Universal Gates (U1-U6)

| Gate | Check | Auto-Fix | Enforcement |
|------|-------|----------|-------------|
| U1 | ≥3 sources, ≥1 academic/authoritative | Fetch from KB | Append before delivery |
| U2 | Disclosure before verdict | Prepend template | Block if missing |
| U3 | Evidence tier labeled per source | Annotate tiers | Tag each source |
| U4 | Language matches preference | Translate | Pre-flight detection |
| U5 | Output template complete | Reformat | Check sections |
| U6 | Claims traceable to source | Flag unsupported | Mark each claim |

### Domain Gates (G1-G4)

| Gate | Check | Auto-Fix | Enforcement |
|------|-------|----------|-------------|
| G1 | Locomotion & collection chosen | Select default | Must specify |
| G2 | Path planning vs tide/current | Apply algorithm | Must address |
| G3 | Autonomy & battery sized | Calculate defaults | Must specify |
| G4 | Reliability (IP rating, corrosion) | Apply standards | Must specify |

---

## Graceful Degradation System

### Degradation Levels

| Level | Condition | Behavior |
|-------|-----------|----------|
| 0 | All sources reachable | Full analysis |
| 1 | Some secondary sources used | Flag substituted sources |
| 2 | Knowledge base only | "Historical context" banner |
| 3 | Missing variables | "DATA UNAVAILABLE" flags |
| 4 | All sources failed | Emit limitation, don't fabricate |

### Limitation Banner

```markdown
---
⚠️ LIMITATION NOTICE
This output was generated with reduced data availability (Level [0-4]).
Cross-check with current data before acting on it.
---
```

---

## Hooks System

### Available Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `pre-flight` | Before execution | Input validation, language detection |
| `pre-step` | Before each step | State verification |
| `post-step` | After each step | Result capture, quality gates |
| `on-error` | On any error | Recovery action determination |
| `on-degrade` | On degradation increase | Limitation emission |
| `post-flight` | After execution | Final validation, formatting |

### Hook Output

All hook events logged to `logs/hooks.log` and `logs/hooks.jsonl`

---

## Structured Logging

### Log Files

- `logs/hooks.log` - Hook system events
- `logs/knowledge_updater.log` - Knowledge crawl logs
- `logs/knowledge_updater.jsonl` - Structured JSON logs
- `logs/knowledge_updater_metrics.json` - Crawl metrics

### Log Levels

- DEBUG: Detailed diagnostic info
- INFO: Normal operations
- WARNING: Degradation or non-critical issues
- ERROR: Failures with recovery
- CRITICAL: Unrecoverable failures

---

## Knowledge Pipeline v2.0

### Enhanced Features

- **Structured logging**: All operations logged with context
- **Better error handling**: Retry with exponential backoff
- **Progress tracking**: Metrics per crawl operation
- **Tier classification**: Automatic evidence tier assignment
- **Deduplication**: SHA256-based DOI/URL dedup

### Crawl Schedule

```cron
# Weekly academic update (Mondays 8:00 AM)
0 8 * * 1 python D:/972026/235-beach-cleaning-robot-design/tools/knowledge_updater_v2.py

# Daily news update (Daily 7:00 AM)
0 7 * * * python D:/972026/235-beach-cleaning-robot-design/tools/knowledge_updater_v2.py --news-only
```

### Manual Execution

```bash
# Full crawl
python tools/knowledge_updater_v2.py

# Dry run
python tools/knowledge_updater_v2.py --dry-run

# Custom keywords
python tools/knowledge_updater_v2.py --keywords "beach robot" "marine litter"
```

---

## Testing v2.0

### Test Scenarios

7 comprehensive test scenarios covering:
1. Standard full analysis (English)
2. Standard full analysis (Vietnamese)
3. Minimal input with defaults
4. Degraded mode (source failures)
5. Comparison scenarios
6. Risk/conflict scenarios
7. Quality gate failure testing

### Running Tests

```bash
# All tests
python tests/test_hooks.py
python tests/test_schema_validator.py

# Test scenarios (manual)
# See tests/test-scenarios_v2.md
```

---

## Sub-Skills (v2.0 Enhanced)

| `sub-gather-requirements` | Intake specialist with schema validation |
| `sub-evidence-collector` | Data librarian with retry & fallback |
| `sub-core-analysis` | Domain expert with structured methods |
| `sub-knowledge-updater` | Research librarian with tier classification |
| `sub-advisor` | Senior advisor with risk disclosure |

---

## Tools Required

- **WebSearch** / **WebFetch** — Domain sources
- **Read** / **Write** — File operations, knowledge base
- **Bash** — Knowledge pipeline execution
- **Skill** — Sub-skill invocation
- **SchemaValidator** — JSON validation (scripts/schema_validator.py)
- **Hooks** — Lifecycle management (scripts/hooks.py)

---

## Output Templates

### English Template
`assets/templates/report-template-en.md`

### Vietnamese Template
`assets/templates/report-template-vi.md`

Both templates include:
- Executive summary
- Inputs & scope
- Evidence collected
- Analysis scorecard
- Performance scenarios
- Action plan
- Academic evidence
- Disclosure (mandatory)
- Recommendation with verdict
- Quality gate checklist

---

## Verdict Categories

| Category | Description | When Used |
|----------|-------------|-----------|
| **Production-Ready Design** | All requirements met, risks addressed | Standard case |
| **Conditional (autonomy)** | Viable but autonomy constraints | Battery/solar limited |
| **Harsh-Environment Risk** | Environmental challenges | Surf zone, harsh conditions |
| **Inconclusive** | Insufficient data | Missing critical inputs |

---

## Active Development Status

- [x] Phase 0: Architecture & Research
- [x] Phase 1: Core Sub-Skills
- [x] Phase 2: Main Harness + Quality Gates
- [x] Phase 3: Knowledge Pipeline
- [x] Phase 4: Testing & Validation
- [x] Phase 5: Integration & Polish v1.0.0
- [x] **Phase 6: Production Upgrade v2.0.0** ✨

### v2.0.0 Enhancements

- [x] Modular directory structure (config/, scripts/, references/, assets/)
- [x] Comprehensive skill registry (SKILL_REGISTRY.md)
- [x] Production-grade hooks system (hooks.py)
- [x] Structured logging (logger.py)
- [x] JSON schema validation (schema_validator.py, schemas/*.json)
- [x] Enhanced knowledge pipeline (knowledge_updater_v2.py)
- [x] Domain reference documentation (domain-methods.md)
- [x] Bilingual templates (report-template-{en,vi}.md)
- [x] Comprehensive test infrastructure (test_*.py, test-scenarios_v2.md)
- [x] Tool definitions (TOOLS.md)
- [x] Hooks documentation (HOOKS.md)

---

## v2.0.0 Production Ready

**Status:** ✨ **PRODUCTION READY v2.0.0** ✨

All 8-file contract requirements met:
- CLAUDE.md ✅ (this file)
- PROJECT-detail.md ✅
- PROJECT-DEVELOPMENT-PHASE-TRACKING.md ✅
- README.md ✅
- skills/main.md ✅ (with 5 sub-skills)
- SECOND-KNOWLEDGE-BRAIN.md ✅
- tools/knowledge_updater.py ✅ (v1 + v2)
- tests/test-scenarios.md ✅ (v1 + v2)

**Plus v2.0 enhancements:**
- config/ directory with schemas and documentation
- scripts/ directory with production utilities
- references/ directory with domain methods
- assets/ directory with templates
- logs/ directory for structured logging
- Enhanced error handling and recovery
- Graceful degradation system
- Structured logging and metrics

---

## References

- `PROJECT-detail.md` — Full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — Build roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — Self-improving knowledge base
- `config/SKILL_REGISTRY.md` — Skill registration system
- `config/TOOLS.md` — Tool definitions
- `config/HOOKS.md` — Hooks documentation
- `references/domain-methods.md` — Domain reference
- `D:\972026\SKILL-STANDARD.md` — Library-wide standard

---

**Version:** 2.0.0
**Last Updated:** 2026-07-27
**Status:** Production Ready ✨
