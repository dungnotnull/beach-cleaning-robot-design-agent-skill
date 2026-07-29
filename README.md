# beach-cleaning-robot-design

**Beach-Cleaning Robot Design (Path Optimization vs Current**

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]())

A production-grade Claude Code harness for **Beach-Cleaning Robotics & Coastal Engineering** — gathers real-time authoritative data, applies recognized domain methods, integrates academic research, and delivers evidence-backed, risk-disclosed outputs with graceful degradation and structured logging.

---

## ✨ v2.0.0 Production Release

### What's New in v2.0.0

**Architecture Enhancements:**
- 🏗️ **Modular directory structure**: config/, scripts/, references/, assets/, logs/
- 📋 **Comprehensive skill registry**: SKILL_REGISTRY.md with execution protocols
- 🔗 **Production hooks system**: Lifecycle hooks for state management and error recovery
- 📊 **Structured logging**: JSON-based logging with metrics tracking
- ✅ **JSON schema validation**: Input/output validation with detailed error reporting

**New Features:**
- 🌐 **Bilingual support**: Full English and Vietnamese output templates
- 📚 **Domain reference documentation**: Comprehensive Beach-Cleaning Robotics methods
- 🔌 **Enhanced tool definitions**: TOOLS.md with schemas and retry policies
- 🎯 **Graceful degradation system**: 5-level degradation with explicit limitation notices
- 📈 **Production-grade knowledge pipeline**: Enhanced crawling with metrics and tier classification

**Quality Improvements:**
- 🛡️ **Production-grade error handling**: Retry with exponential backoff
- 📝 **Comprehensive testing**: 7 test scenarios + unit tests for hooks and schema validation
- 🔍 **Quality gate enforcement**: 10 gates (U1-U6 universal + G1-G4 domain)
- 📋 **Output templates**: Structured reports in English and Vietnamese

---

## Features

### Core Capabilities

- **Real-time data aggregation** from authoritative Beach-Cleaning Robotics sources
- **Systematic domain analysis** using recognized methods (locomotion, sensing, path planning, battery, reliability)
- **Academic research integration** with auto-updating knowledge base
- **Risk/limitation-disclosed outputs** with multi-scenario coverage
- **Self-improving knowledge pipeline** (weekly crawl with metrics)
- **Graceful degradation** with explicit limitation notices
- **Bilingual support** (English and Vietnamese)

### v2.0.0 Architecture

```
├── config/          # Configuration, schemas, documentation
├── scripts/         # Production utilities (hooks, logger, validator)
├── references/      # Domain reference documentation
├── assets/          # Output templates (EN/VI)
├── skills/          # Harness and sub-skills
├── tools/           # Knowledge pipeline (v1 + v2)
├── tests/           # Comprehensive test suite
└── logs/            # Structured logs (generated)
```

---

## Installation

### Prerequisites

- Python 3.11+
- Claude Code with skill support

### Dependencies

```bash
# Core dependencies
pip install requests feedparser python-dateutil

# Optional: JSON schema validation
pip install jsonschema

# Optional: Testing
pip install pytest pytest-cov
```

### Skill Installation

Copy skill files to your Claude skills directory:

```bash
# Option 1: Install directly
cp -r skills/* ~/.claude/skills/

# Option 2: Reference via project CLAUDE.md
# (Already configured in this project)
```

---

## Usage

### Basic Usage

```bash
/beach-cleaning-robot-design

I need to design a beach-cleaning robot for a 2km sandy beach in California.
The beach has moderate slope (5-10 degrees), mixed debris (plastic bottles, cans,
small items). Budget is flexible. Target: maximum coverage per day with solar
assist for autonomy.
```

### Vietnamese Usage

```bash
/beach-cleaning-robot-design

Tôi cần thiết kế robot quét rác cho bãi biển dài 2km tại Nha Trang.
Bãi biển có độ dốc vừa phải (5-10 độ), rác thải hỗn hợp (chai nhựa, lon,
mặt hàng nhỏ). Ngân sách linh hoạt. Mục tiêu: tối đa hóa vùng phủ sóng mỗi ngày
với hỗ trợ năng lượng mặt trời cho tự chủ.
```

---

## Architecture

### Harness Flow

```
[PRE-FLIGHT HOOK]
  ↓
  Language detection → Input validation → Tool check → State init
  ↓
Step 1: sub-gather-requirements → Structured requirements
  ↓
Step 2: sub-evidence-collector → Data bundle (with retry/fallback)
  ↓
Step 3: sub-core-analysis → Domain analysis (locomotion, sensing, battery, reliability)
  ↓
Step 4: sub-knowledge-updater → Academic evidence with tiers
  ↓
Step 5: sub-advisor → Synthesis with disclosure
  ↓
[POST-FLIGHT HOOK]
  ↓
Quality gate validation → Output formatting → Metadata → Delivery
```

### Quality Gates

**Universal Gates (U1-U6):**
- U1: ≥3 sources cited, ≥1 academic/authoritative
- U2: Disclosure/limitations before recommendation
- U3: Evidence hierarchy stated per source (Tier 1–4)
- U4: Language matches user preference
- U5: Output uses declared template (all sections)
- U6: Every claim traceable to ≥1 source or flagged

**Domain Gates (G1-G4):**
- G1: Locomotion & collection mechanism chosen
- G2: Path planning vs tide/current
- G3: Autonomy & battery sized
- G4: Reliability (corrosion/water/sand) planned

### Graceful Degradation

| Level | Condition | Behavior |
|-------|-----------|----------|
| 0 | All sources reachable | Full analysis |
| 1 | Some secondary sources | Flag substituted sources |
| 2 | Knowledge base only | "Historical context" banner |
| 3 | Missing variables | "DATA UNAVAILABLE" flags |
| 4 | All sources failed | Limitation notice |

---

## Data Sources

### Authoritative Sources

- **Robotics references**: ROS, AMR, locomotion on sand
- **Coastal morphology**: Tidal lines, debris patterns
- **Path-planning**: A*, coverage algorithms, boustrophedon
- **Battery/motor**: Energy consumption, solar assist
- **Marine debris**: NOAA, pollution sources
- **Sensors**: LiDAR, camera, debris detection

### Academic Sources

- Journal of Field Robotics — Wiley
- IEEE Transactions on Robotics
- Ocean Engineering — Elsevier
- Marine Pollution Bulletin — Elsevier
- Robotics and Autonomous Systems — Elsevier
- Sensors (MDPI)

---

## Knowledge Base

`SECOND-KNOWLEDGE-BRAIN.md` is auto-updated weekly via `tools/knowledge_updater_v2.py`.

### Manual Update

```bash
# Full crawl (academic + news)
python tools/knowledge_updater_v2.py

# News only
python tools/knowledge_updater_v2.py --news-only

# Dry run
python tools/knowledge_updater_v2.py --dry-run

# Custom keywords
python tools/knowledge_updater_v2.py --keywords "beach robot" "marine litter"
```

### Automated Schedule

```cron
# Weekly academic update (Mondays 8:00 AM)
0 8 * * 1 python D:/972026/235-beach-cleaning-robot-design/tools/knowledge_updater_v2.py

# Daily news update (Daily 7:00 AM)
0 7 * * * python D:/972026/235-beach-cleaning-robot-design/tools/knowledge_updater_v2.py --news-only
```

---

## Testing

### Unit Tests

```bash
# Test hooks system
python tests/test_hooks.py

# Test schema validation
python tests/test_schema_validator.py

# Test knowledge updater
python tools/test_knowledge_updater.py
```

### Integration Tests

See `tests/test-scenarios_v2.md` for 7 comprehensive test scenarios:

1. Standard full analysis (English)
2. Standard full analysis (Vietnamese)
3. Minimal input with defaults
4. Degraded mode (source failures)
5. Comparison scenarios
6. Risk/conflict scenarios
7. Quality gate failure testing

---

## Verdict Categories

| Category | Description | When Used |
|----------|-------------|-----------|
| **Production-Ready Design** | All requirements met, risks addressed | Standard case |
| **Conditional (autonomy)** | Viable but autonomy constraints | Battery/solar limited |
| **Harsh-Environment Risk** | Environmental challenges | Surf zone, harsh conditions |
| **Inconclusive** | Insufficient data | Missing critical inputs |

---

## Output Format

The skill produces structured reports with:

1. **Executive Summary**: 2-3 sentence overview
2. **Inputs & Scope**: Analysis parameters
3. **Evidence Collected**: Current data with source tiers
4. **Analysis / Scorecard**: Domain analysis with scores
5. **Action Plan**: Concrete recommendations
6. **Academic Evidence**: 3-5 citations with tiers
7. **⚠️ Disclosure**: Mandatory limitations notice
8. **Recommendation**: Verdict with scenarios, risks, evidence chain
9. **Quality Gate Checklist**: All gates validated

Templates available in English and Vietnamese.

---

## Configuration

### Key Configuration Files

- `config/SKILL_REGISTRY.md` - Skill registration and execution
- `config/TOOLS.md` - Tool definitions and schemas
- `config/HOOKS.md` - Hooks system documentation
- `config/schemas/*.json` - JSON schemas for validation

### Customization

Edit `KNOWLEDGE_CONFIG` in `tools/knowledge_updater_v2.py` to customize:
- Domain keywords
- ArXiv categories
- RSS feeds
- Scoring weights
- Rate limiting

---

## Roadmap

### Completed

- [x] Phase 0: Architecture & Research
- [x] Phase 1: Core Sub-Skills
- [x] Phase 2: Main Harness + Quality Gates
- [x] Phase 3: Knowledge Pipeline
- [x] Phase 4: Testing & Validation
- [x] Phase 5: Integration & Polish v1.0.0
- [x] **Phase 6: Production Upgrade v2.0.0** ✨

### Future Enhancements (v2.1+)

- [ ] Integration with real-time tide data APIs
- [ ] 3D beach terrain modeling
- [ ] Cost estimation module
- [ ] Environmental impact assessment
- [ ] Multi-robot coordination strategies
- [ ] Web dashboard for visualization

---

## Project Structure

```
beach-cleaning-robot-design/
├── CLAUDE.md                          # Skill identity & usage
├── README.md                          # This file
├── PROJECT-detail.md                  # Technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Build roadmap
├── SECOND-KNOWLEDGE-BRAIN.md          # Self-improving knowledge base
├── config/
│   ├── SKILL_REGISTRY.md              # Skill registration
│   ├── TOOLS.md                       # Tool definitions
│   ├── HOOKS.md                       # Hooks documentation
│   └── schemas/                       # JSON schemas
│       ├── requirements-input.schema.json
│       ├── evidence-output.schema.json
│       ├── core-analysis-output.schema.json
│       └── final-report-output.schema.json
├── scripts/
│   ├── hooks.py                       # Lifecycle hooks
│   ├── schema_validator.py            # JSON validation
│   └── logger.py                      # Structured logging
├── references/
│   └── domain-methods.md              # Domain reference
├── assets/
│   └── templates/
│       ├── report-template-en.md
│       └── report-template-vi.md
├── skills/
│   ├── main.md                        # Main harness
│   ├── sub-gather-requirements.md
│   ├── sub-evidence-collector.md
│   ├── sub-core-analysis.md
│   ├── sub-knowledge-updater.md
│   └── sub-advisor.md
├── tools/
│   ├── knowledge_updater.py           # v1.0 (legacy)
│   ├── knowledge_updater_v2.py        # v2.0 (production)
│   ├── test_knowledge_updater.py
│   └── run_test_scenarios.py
├── tests/
│   ├── test-scenarios.md
│   ├── test-scenarios_v2.md
│   ├── test_hooks.py
│   └── test_schema_validator.py
└── logs/                              # Generated logs
    ├── hooks.log
    ├── knowledge_updater.log
    └── knowledge_updater.jsonl
```

---

## Contributing

Contributions welcome! Please:

1. Read `CONTRIBUTING.md`
2. Run all tests before submitting
3. Follow the 8-File Contract (see `SKILL-STANDARD.md`)
4. Ensure all quality gates pass
5. Update documentation as needed

---

## License

MIT — see LICENSE.

---

## Citation

```bibtex
@software{beach-cleaning-robot-design,
  title = {beach-cleaning-robot-design: Beach-Cleaning Robot Design (Path Optimization vs Current)},
  author = {Claude Code},
  year = {2026},
  version = {2.0.0},
  url = {https://github.com/anthropics/claude-code-skills}
}
```

---

## Why This Skill

Beach-Cleaning Robotics practitioners face:

1. **Data fragmentation**: Authoritative data scattered across sources
2. **Methodology gaps**: Most advice lacks systematic, evidence-based methods
3. **No self-improvement**: Static tools don't learn from new research

This skill unifies:
- ✅ Real-time authoritative data aggregation
- ✅ Recognized domain methods and frameworks
- ✅ Academic research integration
- ✅ Production-grade error handling
- ✅ Graceful degradation with transparency
- ✅ Continuously-updated knowledge base

---

**Version:** 2.0.0
**Status:** Production Ready ✨
**Last Updated:** 2026-07-27
