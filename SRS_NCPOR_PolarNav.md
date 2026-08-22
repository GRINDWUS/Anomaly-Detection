# 🧊 Software Requirements Specification (SRS)
## PolarNav: Uncertainty-Aware Polar Navigation Decision-Support System for Antarctic Research Vessels

---

## 📄 Executive Summary

Navigating research vessels through Antarctic waters requires managing dynamic sea-ice concentrations, shifting iceberg fields, and severe atmospheric forcing. Traditional polar navigation relies heavily on low-frequency satellite observations and manual lookouts. Rapidly changing environmental conditions increase transit times, vessel structural risk, and fuel consumption.

**PolarNav** is an uncertainty-aware decision-support prototype designed to integrate multi-source operational Earth-observation data, forecast environmental risk fields under uncertainty, and optimize multi-objective navigation routes for Antarctic operations.

- **Observe:** Fuses SAR satellite observations, sea-ice concentrations, ocean currents, and wind vectors.
- **Predict:** Combines hydrodynamic baseline kinematics with temporal spatial residual forecasting (Physics-Guided Residual ConvLSTM).
- **Quantify Uncertainty:** Generates spatial uncertainty maps from Monte Carlo drift ensembles, including variance estimates ($\sigma^2$).
- **Optimize:** Evaluates multi-objective navigation profiles balancing vessel ice-interaction risk, fuel efficiency, and forecast uncertainty using Dynamic A*.
- **Explain:** Delivers actionable, quantitative trade-off explanations to vessel officers rather than opaque black-box recommendations.

> **Operational Safety Disclaimer:** PolarNav is a prototype decision-support system intended for tactical route planning. It does not replace certified onboard marine navigation systems, official ice-navigation protocols, or final command authority of ship officers.

---

## 1. 📌 Introduction & Operational Scope

### 1.1 Objective
To develop a decision-support prototype for **NCPOR (National Centre for Polar and Ocean Research)** operational scenarios to optimize passage planning for Indian research vessels (e.g., *ORV Sagar Nidhi*) operating between the Southern Ocean and Indian Antarctic research stations (**Maitri** and **Bharti**).

### 1.2 Dual-Mode Deployment Architecture
- **Primary Mode (NCPOR Mission Control / Cloud):** Heavy spatial ingestion, satellite feature extraction, and multi-day model forecasting performed on cloud infrastructure. Transmits lightweight vector GeoJSON packages (<100 KB) over Iridium/maritime satellite links.
- **Onboard Edge Mode (Vessel Fallback):** Local offline navigation client running on vessel hardware. Executes real-time local path replanning against cached environmental cost grids during communications degradation or blackouts.

---

## 2. 🏗️ High-Level System Architecture

```text
                  POLARNAV ARCHITECTURE
                            │
             ┌──────────────┴──────────────┐
             │       DATA INGESTION        │
             └──────────────┬──────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
   SAR (Sentinel-1)   NSIDC (Ice Conc)   CMEMS (Currents)
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                           ERA5 (Winds)
                            │
                            ▼
                  ENVIRONMENTAL STATE
                            │
       ┌────────────────────┴────────────────────┐
       ▼                                         ▼
 SEA-ICE MODEL                            ICEBERG DRIFT
 (ConvLSTM Residual)                      (Temporal Track + Kinematics)
       │                                         │
       └────────────────────┬───────────┬────────┘
                                        │
                                        ▼
                             PROBABILISTIC RISK FIELD
                           (Monte Carlo Uncertainty σ²)
                                        │
                                        ▼
                            MULTI-OBJECTIVE ROUTER
                             (Dynamic A* Engine)
                                        │
       ┌────────────────────────────────┼────────────────────────────────┐
       ▼                                ▼                                ▼
 SAFEST ROUTE                    BALANCED ROUTE                    FASTEST ROUTE
 (Min Risk Buffer)               (Optimal Trade-off)               (Min Transit Duration)
       │                                │                                │
       └────────────────────────────────┼────────────────────────────────┘
                                        │
                                        ▼
                         DECISION EXPLANATION LAYER
                 (Quantified Risk vs. Fuel vs. Uncertainty Rationale)
                                        │
                                        ▼
                          OFFLINE MARITIME NAVIGATION UI
                        (Vector Leaflet / React Edge Client)
```

---

## 3. 🔬 System Modules & Engineering Specifications

### Module 1: Multimodal Environmental Ingestion & SAR Processing
- **Observation Strategy:** SAR-first observation strategy for high-latitude ocean and ice observation during polar night and cloud-obscured conditions, supplemented by passive microwave and atmospheric datasets.
- **SAR Backscatter Processing:** Polarization-aware SAR preprocessing and backscatter-derived feature extraction adapted to selected Sentinel-1 acquisition modes (e.g., HH/HV or VV/VH).

### Module 2: Physics-Guided Trajectory & Environmental Forecasting
- **Input Data Sources:** CMEMS Ocean Surface Currents (`GLOBAL_ANALYSISFORECAST_PHY_001_024`) + ERA5 10m Surface Winds.
- **Temporal Track & Kinematic Baseline:** Iceberg trajectories are constructed from temporally linked multi-frame observations ($t-3, \dots, t$), with dynamical updates modeled as:
$$\Delta \mathbf{x}_{t+1} = \int_{t}^{t+\Delta t} \left[ \mathbf{v}_{\text{ocean}}(\mathbf{x}, \tau) + \mathbf{v}_{\text{wind\_drift}}(\mathbf{x}, \tau) \right] d\tau + \boldsymbol{\varepsilon}_{\text{ML}}(\mathbf{x}, t)$$
where $\mathbf{v}_{\text{wind\_drift}}$ is a wind-induced drift parameterization calibrated against observed trajectory forcing.
- **Learned Residual Correction & Ensemble:** A **Physics-Guided Residual ConvLSTM** models spatial-temporal residual drift ($\boldsymbol{\varepsilon}_{\text{ML}}$), while **Monte Carlo drift simulations** (sampling wind, current, and positional noise distributions) produce explicit spatial uncertainty grids ($\sigma^2$).

### Module 3: Multi-Objective Route Optimization & Decision Explanation

- **Algorithm:** **Dynamic A*** operating on a discretized 2D risk-cost grid derived from the environmental risk field.
- **Objective Functional:**
$$\mathcal{J}(\pi) = \int_{0}^{T} \left[ w_1 \cdot \mathcal{C}_{\text{fuel}}(v(t), \text{SIC}(\mathbf{x})) + w_2 \cdot \mathcal{R}_{\text{ice}}(\text{SIC}(\mathbf{x}), \mathbf{d}_{\text{iceberg}}) + w_3 \cdot \mathcal{U}_{\text{forecast}}(\mathbf{x}, t) \right] dt$$

- **Surrogate Hydrodynamic Fuel Model:** Parameterized by vessel displacement, speed, and local sea-ice concentration ($SIC$).
- **Decision Explanation Layer:** Quantifies the rationale for each route by reporting relative changes in predicted ice-interaction risk, estimated fuel consumption, transit duration, and forecast uncertainty compared with alternative routes.

---

## 4. ⚠️ Technical Risk Mitigation & Solutions Matrix

| Operational Challenge | Root Cause | Engineering Solution |
| :--- | :--- | :--- |
| **Polar Night & Cloud Cover** | Optical satellite bands blinded in winter | SAR-first pipeline using polarization-aware C-band SAR. |
| **SAR Speckle Backscatter Noise** | Wave clutter causes false iceberg alarms | SAR speckle filtering and polarization-aware backscatter features adapted to acquisition mode. |
| **Bandwidth Limits at Sea** | High latency satellite links (<100 kbps) | Cloud generates compressed tiny GeoJSON vector route packages (<100 KB). |
| **Non-linear Environmental Drift** | Pure linear momentum ignores hydrodynamic drag | Physical kinematic baseline coupled with spatial ConvLSTM residual learning. |
| **Unrealistic Vessel Maneuvers** | Grid pathfinding generates sharp turns | Dynamic A* path smoothing constrained by vessel turning radius & inertia. |
| **Communications Blackout** | Vessel loses satellite connectivity | Edge client executes autonomous local route replanning on cached risk maps. |

---

## 5. 📊 Validation Hierarchy & Target Benchmarks

### 5.1 Validation Data Hierarchy
1. **Proposed Primary Validation:** Historical Antarctic iceberg drift tracks (Pending exact dataset ID verification: e.g., *BYU Antarctic Iceberg Tracking Database / NSIDC Iceberg Tracking Repository*).
2. **Secondary Validation:** Synthetic benchmark drift trajectories generated from observed environmental forcing.
3. **Auxiliary Validation:** Oceanographic buoy drift data for isolating ocean current drag parameters.

### 5.2 Target Benchmarks for System Validation

| Metric | Target Engineering Goal | Validation Strategy |
| :--- | :--- | :--- |
| **Iceberg Segmentation Accuracy** | Target IoU $> 85\%$ | Benchmark against annotated C-CORE / Statoil image patches |
| **72h Trajectory Displacement** | Target Mean Error $< 10\text{ km}$ | Primary validation against historical Antarctic iceberg tracks |
| **Transmitted Route Payload Size** | Target $< 100\text{ KB}$ | Serialized GeoJSON vector payload size verification |
| **Path Computation Latency** | Target $< 15\text{ seconds}$ | Benchmark Dynamic A* replanning speed on $500 \times 500$ grids |
| **Operational Efficiency Impact** | Quantitative Fuel / Distance Trade-off | Comparative simulation against baseline direct A* pathfinding |

---

<div align="center">

**PolarNav Engineering Specification | Smart India Hackathon 2026**  
*National Centre for Polar and Ocean Research (NCPOR)*

</div>
