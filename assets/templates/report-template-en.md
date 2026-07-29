# Beach-Cleaning Robot Design (Path Optimization vs Current) — Report

**Date:** {{date}} | **Analyst:** beach-cleaning-robot-design v{{version}} | **Language:** {{language}} | **Domain:** Beach-Cleaning Robotics & Coastal Engineering

---

## Executive Summary

[2–3 sentences; verdict + headline action]

---

## Inputs & Scope

**Object of Analysis:** {{object}}

**Scope:** {{scope}}

**Timeframe:** {{timeframe}}

**Available Inputs:** {{available_inputs}}

**Target Audience:** {{target_audience}}

**Analysis Type:** {{analysis_type}}

---

## Evidence Collected

### Current Data & Parameters

| Source | Data Point | Value | Tier |
|--------|------------|-------|------|
{{current_data_rows}}

### Authoritative Documents

{{authoritative_docs}}

### Recent Developments

{{recent_news}}

---

## Analysis / Scorecard

### Locomotion & Collection

**Selected Configuration:** {{locomotion_type}} + {{collection_mechanism}}

**Specification:**
- Wheel/Track spec: {{wheel_track_spec}}
- Clearance: {{clearance_mm}}mm
- Slope capability: {{slope_degrees}}°
- Collection mesh: {{sieve_mesh_mm}}mm

**Rationale:** {{locomotion_rationale}}

**Score:** {{locomotion_score}}/100

---

### Sensing & Path Planning

**Sensors:**
{{sensors_list}}

**Algorithm:** {{path_algorithm}}

**Tide/Current Aware:** {{tide_aware}}

**Coverage Efficiency:** {{coverage_efficiency}}%

**Score:** {{sensing_score}}/100

---

### Battery & Autonomy

**Battery Capacity:** {{capacity_wh}} Wh

**Autonomy:** {{autonomy_hours}} hours

**Solar Assist:** {{solar_assist}}

**Consumption Breakdown:**
- Locomotion: {{locomotion_percent}}%
- Sensing: {{sensing_percent}}%
- Collection: {{collection_percent}}%
- Computing: {{computing_percent}}%

**Score:** {{battery_score}}/100

---

### Reliability

**IP Rating:** {{ip_rating}}

**Corrosion Protection:** {{corrosion_protection}}

**Water Ingress Protection:** {{water_protection}}

**Sand Abrasion Resistance:** {{sand_resistance}}

**Self-Righting:** {{self_righting}}

**Maintenance Interval:** {{maintenance_interval}} hours

**MTBF:** {{mtbf}} hours

**Score:** {{reliability_score}}/100

---

### Performance Scenarios

| Scenario | Conditions | Coverage Rate (m²/h) | Collection Efficiency (%) |
|----------|------------|----------------------|---------------------------|
| **Best** | {{best_conditions}} | {{best_coverage}} | {{best_efficiency}} |
| **Base** | {{base_conditions}} | {{base_coverage}} | {{base_efficiency}} |
| **Worst** | {{worst_conditions}} | {{worst_coverage}} | {{worst_efficiency}} |

---

## Action / Control Plan

{{action_plan}}

---

## Academic & Research Evidence

{{academic_evidence}}

---

## ⚠️ Disclosure / Limitations

> {{disclosure_text}}

---

## Recommendation / Conclusion

**Verdict:** {{verdict}}

**Confidence:** {{confidence}}

### Key Risks

{{key_risks}}

### Evidence Chain

{{evidence_chain}}

### Remediation

{{remediation}}

---

## Post-Execution Gate Checklist

**Universal Gates:**
- [U1] ≥3 sources cited, ≥1 academic/authoritative: {{U1_status}}
- [U2] Disclosure/limitations before recommendation: {{U2_status}}
- [U3] Evidence hierarchy stated per source: {{U3_status}}
- [U4] Language matches user preference: {{U4_status}}
- [U5] Output uses declared template: {{U5_status}}
- [U6] Every claim traceable to ≥1 source: {{U6_status}}

**Domain Gates:**
- [G1] Locomotion & collection mechanism chosen: {{G1_status}}
- [G2] Path planning vs tide/current: {{G2_status}}
- [G3] Autonomy & battery sized: {{G3_status}}
- [G4] Reliability (corrosion/water/sand) planned: {{G4_status}}

**Limitations Flagged:**
{{limitations}}

---

**Report Generated:** {{timestamp}} | **Execution ID:** {{execution_id}} | **Duration:** {{duration_ms}}ms
