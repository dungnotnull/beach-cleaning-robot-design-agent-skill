# Test Scenarios v2.0.0 — Skill 235: beach-cleaning-robot-design

Comprehensive end-to-end test scenarios for production validation.

---

## Test Philosophy

These scenarios validate:
1. **Functional correctness**: Each skill produces expected outputs
2. **Quality gate enforcement**: All gates are checked and enforced
3. **Error handling**: Graceful degradation and recovery
4. **Language support**: Vietnamese and English outputs
5. **Edge cases**: Minimal inputs, conflicting data, source failures

---

## Scenario 1: Standard Full Analysis (English)

### Input
```
/beach-cleaning-robot-design

I need to design a beach-cleaning robot for a 2km sandy beach in California.
The beach has moderate slope (5-10 degrees), mixed debris (plastic bottles, cans,
small items). Budget is flexible. Target: maximum coverage per day with solar
assist for autonomy.
```

### Expected Steps
1. `sub-gather-requirements`: Extracts object (robot design), scope (California beach), constraints (slope, debris type, solar assist)
2. `sub-evidence-collector`: Fetches current beach cleaning methods, robotics references
3. `sub-core-analysis`: Produces locomotion, sensing, battery, reliability recommendations
4. `sub-knowledge-updater`: Surfaces academic citations with Tier labels
5. `sub-advisor`: Synthesizes into Production-Ready Design verdict
6. Quality gate: All U1-U6 and G1-G4 gates pass

### Expected Outputs
- Locomotion: Wheels or tracks selected with rationale
- Sensing: CNN camera + LiDAR for debris detection
- Path: Boustrophedon coverage with tide-aware replanning
- Battery: Sized for 6-8 hours with solar assist
- Reliability: IP67 rating, corrosion protection specified
- Scenarios: Best/base/worst coverage rates provided

### Gates Validated
- U1: ≥3 sources cited, ≥1 academic
- U2: Disclosure present before verdict
- U3: Evidence tiers labeled
- U4: Language = English
- U5: All template sections present
- U6: All claims sourced or flagged
- G1: Locomotion chosen
- G2: Path planning specified
- G3: Battery sized
- G4: Reliability planned

---

## Scenario 2: Standard Full Analysis (Vietnamese)

### Input
```
/beach-cleaning-robot-design

Tôi cần thiết kế robot quét rác cho bãi biển dài 2km tại Nha Trang.
Bãi biển có độ dốc vừa phải (5-10 độ), rác thải hỗn hợp (chai nhựa, lon,
mặt hàng nhỏ). Ngân sách linh hoạt. Mục tiêu: tối đa hóa vùng phủ sóng mỗi ngày
với hỗ trợ năng lượng mặt trời cho tự chủ.
```

### Expected Steps
Same as Scenario 1, but all output in Vietnamese.

### Expected Outputs
- All section headers translated
- Technical terms kept in English (IP rating, CNN, LiDAR)
- Language detection: vi
- Output uses Vietnamese template

### Gates Validated
- All gates from Scenario 1
- U4: Language = Vietnamese

---

## Scenario 3: Minimal Input (Defaults Applied)

### Input
```
/beach-cleaning-robot-design

Design a beach cleaning robot.
```

### Expected Steps
1. `sub-gather-requirements`: Applies defaults with explicit assumptions
2. Rest of pipeline proceeds with assumed values

### Expected Outputs
- Assumptions explicitly stated (e.g., "Assuming medium-sized sandy beach")
- Default scope: "General beach-cleaning robot design"
- Default analysis_type: "combined"
- No fabricated values - missing fields marked as "DEFAULT ASSUMED"

### Gates Validated
- U6: Assumptions flagged as analyst judgment
- All other gates pass with assumptions noted

---

## Scenario 4: Degraded Mode (Source Failures)

### Input
Simulate network failures for WebSearch/WebFetch.

### Expected Steps
1. `sub-evidence-collector`: Primary sources fail → falls back to knowledge base
2. Degradation Level 2: Uses SECOND-KNOWLEDGE-BRAIN.md only
3. LIMITATION banner emitted
4. Analysis proceeds with available data

### Expected Outputs
```
---
⚠️ LIMITATION NOTICE
This output was generated with reduced data availability (Level 2).
Reason: Primary network sources unreachable. Using cached knowledge base as of 2026-07-27.
Cross-check with current data before acting on it.
---
```
- Analysis based on cached knowledge
- Verdict may be Inconclusive if data is insufficient
- All sourced entries marked with date stamps

### Gates Validated
- U2: Limitation notice present
- Degradation protocol executed
- No values fabricated

---

## Scenario 5: Comparison Scenario

### Input
```
/beach-cleaning-robot-design

Compare: wheels vs tracks for beach-cleaning robot locomotion on soft sand beach.
```

### Expected Steps
1. `sub-gather-requirements`: Identifies comparison request
2. `sub-evidence-collector`: Fetches data on both options
3. `sub-core-analysis`: Analyzes both locomotion types
4. `sub-advisor`: Provides side-by-side comparison

### Expected Outputs
| Aspect | Wheels | Tracks |
|--------|--------|--------|
| Traction | Lower on soft sand | Higher |
| Maintenance | Lower | Higher |
| Cost | Lower | Higher |
| Recommendation | Best for firm sand | Best for soft sand |

### Gates Validated
- U3: Evidence tiers shown for each source
- U6: Claims traceable to sources
- G1: Both options analyzed

---

## Scenario 6: Risk/Conflict Scenario

### Input
```
/beach-cleaning-robot-design

Design robot for surf zone with heavy debris load and harsh wave action.
```

### Expected Steps
1. Analysis identifies conflicting requirements (delicate electronics vs harsh environment)
2. Multiple scenarios generated
3. Risk disclosure prominent

### Expected Outputs
- Verdict: "Harsh-Environment Risk" or "Conditional"
- Three scenarios: Best (calm conditions), Base (moderate), Worst (heavy surf)
- Key risks section prominent
- Alternative approaches suggested

### Gates Validated
- U2: Risk disclosure before verdict
- G4: Reliability concerns addressed
- Multi-scenario output provided

---

## Scenario 7: Quality Gate Failure (Auto-Fix Test)

### Input
```
/beach-cleaning-robot-design

Quick analysis needed.
```

### Expected Steps
1. Initial analysis may miss some quality gates
2. Auto-fix attempts to add missing elements
3. If auto-fix fails after 2 retries, limitation emitted

### Expected Outputs
- If auto-fix succeeds: Full report with all gates passing
- If auto-fix fails: Report with limitation notice for failed gates
- Example: "U1 failed: Only 2 sources found (required: ≥3)"

### Gates Validated
- Auto-fix mechanism tested
- Gate enforcement verified
- Limitation emission works

---

## Test Execution

### Running Tests

```bash
# Run all scenarios
python tools/run_test_scenarios_v2.py --all

# Run specific scenario
python tools/run_test_scenarios_v2.py --scenario 1

# Verbose output
python tools/run_test_scenarios_v2.py --all --verbose

# Generate coverage report
python tools/run_test_scenarios_v2.py --all --coverage
```

### Test Results Format

```json
{
  "scenario_id": 1,
  "scenario_name": "Standard Full Analysis (English)",
  "passed": true,
  "duration_ms": 23456,
  "quality_gates": {
    "U1": {"passed": true, "attempts": 1},
    "U2": {"passed": true, "attempts": 1},
    "U3": {"passed": true, "attempts": 1},
    "U4": {"passed": true, "attempts": 1},
    "U5": {"passed": true, "attempts": 1},
    "U6": {"passed": true, "attempts": 1},
    "G1": {"passed": true, "attempts": 1},
    "G2": {"passed": true, "attempts": 1},
    "G3": {"passed": true, "attempts": 1},
    "G4": {"passed": true, "attempts": 1}
  },
  "output_sections": ["executive_summary", "inputs_scope", ...],
  "language_detected": "en",
  "verdict": "Production-Ready Design",
  "errors": [],
  "warnings": []
}
```

---

## Coverage Matrix

| Scenario | U1 | U2 | U3 | U4 | U5 | U6 | G1 | G2 | G3 | G4 | Degradation | Language |
|----------|----|----|----|----|----|----|----|----|----|----|-------------|----------|
| 1. Standard (EN) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No | EN |
| 2. Standard (VI) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No | VI |
| 3. Minimal Input | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No | EN |
| 4. Degraded | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Yes | EN |
| 5. Comparison | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | No | EN |
| 6. Risk/Conflict | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No | EN |
| 7. Gate Failure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No | EN |

---

## Success Criteria

All tests pass if:
1. All quality gates validate correctly (enforcement works)
2. Degradation triggers at correct levels
3. Language detection and translation work
4. Auto-fix attempts when appropriate
5. Limitation notices emitted when required
6. No values fabricated - all assumptions flagged
7. Output templates correctly applied

---

*Last Updated: 2026-07-27*
