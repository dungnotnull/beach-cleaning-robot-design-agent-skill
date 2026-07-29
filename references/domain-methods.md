# Domain Methods Reference

## Beach-Cleaning Robotics & Coastal Engineering

Comprehensive reference for domain-specific methods and frameworks used in this skill.

---

## 1. Locomotion & Collection Mechanisms

### 1.1 Wheel vs Track Selection

**Decision Framework:**

| Factor | Wheels Preferred | Tracks Preferred |
|--------|-----------------|------------------|
| Sand firmness | Firm, compact sand | Soft, loose sand |
| Slope | <15° | >15° |
| Sinkage risk | Low | High |
| Maintenance | Low | High |
| Cost | Lower | Higher |

**Key Formulas:**

```
Sinkage (z) = (3W / (2bLγ))^(1/3)
Where:
- W = Vehicle weight (N)
- b = Wheel/track width (m)
- L = Wheel/track contact length (m)
- γ = Soil specific weight (N/m³)
```

**References:**
- Bekker theory for off-road locomotion
- Terramechanics for wheeled vehicles on sand

### 1.2 Collection Mechanisms

| Mechanism | Best For | Limitations |
|-----------|---------|-------------|
| Sieve (sifting) | Small debris (<50mm) | Clogging, energy intensive |
| Gripper | Large debris (>100mm) | Single-item operation |
| Conveyor | Continuous collection | Size sorting needed |
| Suction | Light debris | Limited capacity |

---

## 2. Sensing & Path Planning

### 2.1 Debris Detection

**Sensor Comparison:**

| Sensor | Range | Accuracy | Power | Weather Sensitivity |
|--------|-------|----------|-------|---------------------|
| Camera (RGB) | 5-20m | Medium (85%) | Low | High |
| LiDAR | 10-100m | High (95%) | Medium | Medium |
| Radar | 20-200m | Low (70%) | High | Low |

**CNN Model for Debris Detection:**
```
Input: 224x224x3 RGB image
Backbone: MobileNetV2 (lightweight for edge)
Output: Bounding boxes + class (plastic, metal, organic)
Expected mAP: 0.75+
```

### 2.2 Coverage Path Planning

**Algorithm Comparison:**

| Algorithm | Coverage Efficiency | Computational Cost | Adaptability |
|-----------|---------------------|--------------------|--------------|
| Boustrophedon | 95% | Low | Static |
| Spiral | 85% | Low | Semi-adaptive |
| Adaptive Tide-Aware | 90% | High | Dynamic |

**Tide-Aware Path Planning:**
```
1. Detect high-tide line (via visual markers or local tide data)
2. Define safety buffer from tide line (typical: 2-5m)
3. Replan paths periodically (every 15-30 min)
4. Prioritize areas above high-tide mark
```

**Key Metrics:**
- Coverage rate: m²/hour
- Overlap ratio: % of area revisited
- Energy per unit area: Wh/m²

---

## 3. Battery & Autonomy

### 3.1 Energy Consumption Breakdown

**Typical Distribution:**
- Locomotion: 60-70%
- Collection mechanism: 10-15%
- Sensing/computing: 10-15%
- Communication: 5-10%

**Energy Estimation Formula:**
```
E_total = (P_locomotion + P_collection + P_sensing + P_comms) × t_operation

Where:
- P = Power consumption (Watts)
- t = Operation time (hours)
```

### 3.2 Solar Assist Integration

**Solar Panel Sizing:**
```
P_solar_needed = (E_total - E_battery) / t_sunlight
Where:
- E_total = Total energy required (Wh)
- E_battery = Battery capacity (Wh)
- t_sunlight = Available sunlight hours (typically 4-6h/day)
```

**Typical Configurations:**
| Robot Size | Battery Capacity | Solar Panel | Autonomy |
|------------|------------------|-------------|-----------|
| Small (50kg) | 500Wh | 100W | 4-6h |
| Medium (200kg) | 2000Wh | 400W | 6-8h |
| Large (500kg) | 5000Wh | 1000W | 8-12h |

---

## 4. Reliability & Environmental Protection

### 4.1 IP Rating Selection

| Application | Minimum IP Rating | Rationale |
|-------------|-------------------|-----------|
| Dry sand | IP54 | Dust protection |
| Wet sand/splash | IP65 | Water jet protection |
| Near surf | IP67 | Temporary immersion |
| Surf zone | IP68 | Continuous immersion protection |

### 4.2 Corrosion Protection

**Materials Selection:**
- **Frame:** Marine-grade aluminum (5052, 6061) or stainless steel (316)
- **Fasteners:** 316 stainless or Monel
- **Coatings:** Powder coating, epoxy paints, anodization (for aluminum)

**Protection Methods:**
1. **Sacrificial Anodes:** Zinc or aluminum blocks for cathodic protection
2. **Sealing:** Conformal coating on electronics
3. **Design:** Avoid crevices where salt can accumulate

### 4.3 Sand Abrasion Resistance

**Vulnerable Components:**
- Moving joints
- Tracks/tires
- Sensors (exposed lenses)
- Collection mechanism intake

**Protection Strategies:**
- Hardened seals (polyurethane, rubber)
- Replaceable wear surfaces
- Protective housings for sensors
- Regular maintenance schedule

---

## 5. Performance Metrics & Scenarios

### 5.1 Key Performance Indicators (KPIs)

| KPI | Measurement | Typical Target |
|-----|-------------|-----------------|
| Coverage rate | m²/hour | 500-2000 |
| Collection efficiency | % of debris collected | 70-90% |
| Energy efficiency | Wh/m² | 5-20 |
| Uptime | % | 85-95% |
| MTBF | hours | 200+ |

### 5.2 Scenario Modeling

**Best Case:**
- Flat, firm beach
- Low debris density
- Sunny weather (solar assist)
- Expected: 1500-2000 m²/hour

**Base Case:**
- Moderate slope, mixed sand
- Medium debris density
- Overcast conditions
- Expected: 1000-1500 m²/hour

**Worst Case:**
- Steep, soft sand
- High debris density (clogging risk)
- Wet/rainy conditions
- Expected: 500-1000 m²/hour

---

## 6. Standards & Compliance

### 6.1 Relevant Standards

| Standard | Organization | Coverage |
|----------|---------------|----------|
| ISO 9001 | ISO | Quality management |
| IP ratings | IEC 60529 | Ingress protection |
| EMC | FCC/CE | Electromagnetic compatibility |
| Safety | ISO 12100 | Machinery safety |

### 6.2 Environmental Considerations

- **Noise pollution:** < 65 dB at 10m (typical)
- **Emissions:** Zero direct emissions (electric)
- **Habitat disturbance:** Minimize operation during sensitive periods

---

*Last Updated: 2026-07-27*
