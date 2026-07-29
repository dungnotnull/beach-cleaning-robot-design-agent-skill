# SECOND-KNOWLEDGE-BRAIN.md — Skill 235: beach-cleaning-robot-design

> **Living Knowledge Base** — updated by `tools/knowledge_updater.py` on a weekly
> schedule. All entries date-stamped; new entries appended at the bottom.
> Evidence hierarchy: Systematic Review > Meta-Analysis > Guideline/RCT > Cohort > Expert Consensus > News.

---

## 1. Core Concepts & Frameworks

### 1.1 Beach-Cleaning Robotics & Coastal Engineering — Foundational Methods

### 1.1 Locomotion/collection
Wheels vs tracks on sand (traction, sinkage), sieve (sifting sand) vs gripper for large debris; slope climbing.
### 1.2 Sensing/path
Vision (CNN debris detection), LiDAR obstacle; coverage path planning (boustrophedon), tide-line following, current-aware replanning.
### 1.3 Autonomy
Battery energy (traction, sensing), solar assist, recharging, autonomy time.
### 1.4 Reliability
Corrosion protection (IP rating, seals), salt/water ingress, sand abrasion, self-righting, maintenance.

Knowledge categories covered:
- Locomotion on sand (wheels/tracks)
- Debris sensing (vision, LiDAR)
- Coverage path planning vs tide/current
- Battery/energy & autonomy
- Collection mechanism (sieve, gripper)
- Reliability (salt, water, sand)

### 1.2 Evidence Hierarchy (this domain)
- **Tier 1**: Systematic review / meta-analysis / official standard (ISO, IAWA, CITES, FSC, WHO, UNESCO…)
- **Tier 2**: Peer-reviewed academic paper / RCT
- **Tier 3**: Industry report / professional association guideline
- **Tier 4**: News / blog / vendor material

---

## 2. Key Research Papers & Standards

| Title | Authors | Year | Venue | DOI/URL | Tier |
|------|---------|------|-------|---------|------|
| Coverage path planning | Galceran & Carreras | 2013 | Robotics | 10.1007/s10514-012-9318-4 | 1 |
| Does gamification work? | Hamari et al. | 2014 | Comput. Hum. Behav. | 10.1016/j.chb.2014.03.006 | 2 |
| Beach litter detection (CNN) | Fossati et al. | 2018 | Sensors | 10.3390/s18051538? | 2 |
| Field robotics review | Tuna et al. | 2016 | J. Field Robot. | 10.1002/rob.21624? | 2 |

Authoritative sources registered:
- Journal of Field Robotics — Wiley
- IEEE Transactions on Robotics
- Ocean Engineering — Elsevier
- Marine Pollution Bulletin — Elsevier
- Robotics and Autonomous Systems — Elsevier
- Sensors (MDPI)

---

## 3. State-of-the-Art Methods & Tools

State of the art: CNN debris detection, AMR coverage planning, solar-assist autonomy, modular collection, ruggedized marine robots. Crawl targets: J. Field Robot., IEEE TRO, Ocean Eng., Mar. Pollut. Bull., Sensors.

---

## 4. Authoritative Data Sources

### 4.1 Domain authoritative sources
- Robotics references (ROS, AMR)
- Coastal morphology references (tidal line, debris)
- Path-planning references (A*, coverage)
- Battery/motor references
- Marine debris references (NOAA)
- Sensors (LiDAR, camera) references

### 4.2 Academic & research sources
- Journal of Field Robotics — Wiley
- IEEE Transactions on Robotics
- Ocean Engineering — Elsevier
- Marine Pollution Bulletin — Elsevier
- Robotics and Autonomous Systems — Elsevier
- Sensors (MDPI)

---

## 5. Analytical Frameworks

Knowledge categories covered:
- Locomotion on sand (wheels/tracks)
- Debris sensing (vision, LiDAR)
- Coverage path planning vs tide/current
- Battery/energy & autonomy
- Collection mechanism (sieve, gripper)
- Reliability (salt, water, sand)

Cross-reference the sub-skill workflows in `skills/*.md` for the domain methods applied at each step. The fixed bookends (requirements â†’ evidence â†’ knowledge â†’ synthesis â†’ quality gate) are mandatory; the core analysis sub-skills implement the domain-specific methods.

---

## 6. Self-Update Protocol

- **Crawl pipeline:** `tools/knowledge_updater.py`
- **Schedule:** weekly academic (Mondays 08:00) + daily news (07:00); documented in `CLAUDE.md`
- **Dedup:** SHA256 of DOI/URL (case/whitespace-insensitive)
- **Scoring:** composite 0â€“10 = recency(0.4) + keyword_relevance(0.4) + citation_count(0.2)
- **Crawl targets:** ArXiv categories []; Semantic Scholar keyword clusters; RSS feeds []
- **Gap-fill:** sub-knowledge-updater flags missing values as crawl queries
- **Append rule:** new entries appended under Section 7 with date stamp + relevance score

---

## 7. Knowledge Update Log

_(Appended automatically by the crawl pipeline. Baseline seeded with the references in Section 2.)_
