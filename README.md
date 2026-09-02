# 🛡️ AstraGuard 2.4 — Staged Semiconductor Prognostic Platform

> **Smart India Hackathon 2026 Submission** | **Problem Statement #26170 (ISRO - Space Application Centre)**  
> *Physics-Informed Semiconductor Burn-in Screening & 96h Degradation Forecasting Engine*

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-black.svg)](https://nextjs.org)
[![Test Suite](https://img.shields.io/badge/Tests-23%2F23%20Passed-brightgreen.svg)]()
[![ISRO PS Compliance](https://img.shields.io/badge/ISRO%20PS-%2326170-orange.svg)]()

---

## 📖 Executive Summary & Core Breakthrough

**AstraGuard 2.4** is an aerospace-grade reliability platform designed for qualification burn-in screening of spaceflight microelectronics (MIL-STD-883 Method 1015, AEC-Q100).

Traditional qualification protocols require static **168-hour high-temperature thermal stress testing**, consuming immense electrical energy, chamber time, and ATE operator bandwidth. AstraGuard 2.4 replaces fixed static thresholds with a **Staged Prognostic Engine** that analyzes early 0h, 24h, and 96h telemetry kinetics to forecast 168h degradation trajectories ($R^2 = 0.9913$).

### Key Impact Metrics:
* 🚀 **42.8% – 53.4% Reduction in Thermal Chamber Hours**: Early 96-hour exit for nominal components saves 72 hours per lot.
* 🛡️ **0.0% Defect Escape Rate**: 100% detection recall across critical physical failure mechanisms (Thermal Runaway, Spatial Outliers, Dark Current Spikes).
* ⚡ **29.39% Prediction Error Reduction**: Upgrading from a 24h to a 96h feature horizon ($dI/dt, d^2I/dt^2$) drastically improves forecast precision.

---

## 🏗️ System Architecture

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                     ASTRA GUARD 2.4 SYSTEM ARCHITECTURE                     │
 └─────────────────────────────────────────────────────────────────────────────┘

    [ATE Hardware Telemetry / CSV Ingestion]
                     │
                     ▼
    [AstraGuard SDK Data Integrity Validator] ──▶ (Catch SMU / Instrument Faults)
                     │
                     ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ STAGE A (0h + 24h): Population Outlier Screening                         │
  │ • Robust Median / MAD Z-Score Screener (Z >= 3.5)                         │
  │ • Initial Thermal Runaway & Spatial Wafer Outlier Isolation               │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ STAGE B (0h + 24h + 96h): Physics-Informed Degradation Forecasting       │
  │ • Kinetic Velocity & Acceleration Extraction (dI/dt, d²I/dt²)            │
  │ • Device-Specific Regressors (Digital IC, Mixed-Signal, MEMS, Sensors)    │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ 3-TIER DECISION FUSION & RISK ENGINE                                      │
  │  🟢 GREEN (Auto-Pass at 96h)   -> Exit Chamber Early (Save 72h)           │
  │  🟡 YELLOW (Extend to 168h)    -> Marginal Drift / Safety Interlock       │
  │  🔴 RED (Early Reject at 24/96h)-> Malfunctioning / Rapid Degradation     │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
    [Game-Theoretic SHAP Engine]                       [FastAPI REST & WS Server]
    (Physics Mechanism Attribution)                    (Port 8000)
             │                                                     │
             └──────────────────────────┬──────────────────────────┘
                                        ▼
                           [Next.js Operator Dashboard]
                           (Port 3000 - Live Streaming UI)
```

---

## 📊 Blind Test Validation Matrix (12,000 Components)

Evaluated on the frozen, unseen **`ASQD_2.4`** blind test dataset across 5 core spaceflight microelectronics families:

| Device Family | Upper Spec Limit (USL) | Baseline MAE (24h) | AstraGuard MAE (96h) | $R^2$ Score | Defect Recall | Safety Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DIGITAL_IC** | 1150.0 µA | 40.80 µA | **29.19 µA** | **0.9797** | **100.0%** | Auto-Pass at 96h |
| **MIXED_SIGNAL_IC** | 1150.0 µA | 52.71 µA | **37.87 µA** | **0.9587** | **98.3%** | Extended Burn-in |
| **IMAGE_SENSOR** | 25.0 nA/cm² | 19.89 nA | **1.71 nA** | **0.9655** | **100.0%** | Auto-Pass at 96h |
| **MEMS_GYROSCOPE** | 25.0 deg/hr | 0.0112 deg | **0.0026 deg** | **0.9948** | **Safety Interlock** | Route to `YELLOW` |
| **PRECISION_VOLTAGE_REF** | 6800.0 µV | 415.93 µV | **304.62 µV** | **0.9188** | **100.0%** | Auto-Pass at 96h |

---

## ⚡ Quick Start Guide

### 1. Prerequisites & Installation
Ensure Python 3.11+ and Node.js 18+ are installed.

```bash
# Clone the repository
git clone https://github.com/GRINDWUS/Anomaly-Detection.git
cd Anomaly-Detection

# Install Python dependencies
pip install -r requirements.txt

# Install AstraGuard SDK in editable mode
pip install -e .
```

### 2. Run the Full Unit Test Suite (23/23 Passing)
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 3. Launch the FastAPI Backend Server
```bash
python server.py
```
*Backend interactive OpenAPI docs available at: `http://127.0.0.1:8000/docs`*

### 4. Launch the Next.js Operator Dashboard
```bash
cd dashboard
npm install
npm run dev
```
*Access the live interactive operator dashboard at: `http://localhost:3000`*

### 5. Run Live REST API Validation Script
```bash
python validation/test_api_endpoints.py
```

### 6. Run Complete Research & Analysis Suite
```bash
# Horizon comparison (24h vs 96h)
python validation/compare_telemetry_horizons.py

# SHAP feature attribution audit
python validation/shap_analysis.py

# Failure mode recall audit
python validation/failure_mode_audit.py
```

---

## 🛠️ AstraGuard SDK Integration

Developers and ATE engineers can integrate AstraGuard directly into Python test scripts:

```python
from astraguard_sdk import AstraGuardSDK

# Initialize SDK with read-only ATE telemetry source
sdk = AstraGuardSDK(data_source="ASQD_2.4/asqd_24_blind_test.csv")

# Run staged screening on Digital IC lot
results = sdk.analyze_lot(lot_id="LOT_2026_07", device_family="DIGITAL_IC")

print(f"Total Components : {results['total_components']}")
print(f"Green Pass (96h) : {results['green_pass_count']}")
print(f"Chamber Hours Saved: {results['chamber_hours_saved_percent']}%")
```

---

## 🎖️ ISRO Defense & Standard Compliance

* **MIL-STD-883 Method 1015**: Compliant staged burn-in protocol with decision audit logging.
* **MIL-HDBK-217F**: Reliability prediction integration via kinetic Arrhenius/Black acceleration factors.
* **AEC-Q100 Grade 0/1**: Stress qualification framework support for automotive/aerospace ICs.
* **Game-Theoretic Explainability**: Every decision backed by SHAP feature attribution reason codes.

---

## 📁 Key Repository Structure

```text
├── astraguard_core/            # Core Physics, Module A, Module B & SHAP Engines
│   ├── module_a/               # Robust Z-Score Screener
│   ├── module_b/               # Device-Specific Trajectory Regressors & Registry
│   ├── explainability/         # SHAP Physics Engine (Lazy Loaded)
│   └── feature_engineering/    # Kinetic Feature Extraction (0h, 24h, 96h)
├── astraguard_sdk/             # Python & C ATE Telemetry Integration SDK
├── dashboard/                  # Next.js 14 Web Application & WebSocket Client
├── models/v2/                  # Frozen Model Binaries & Optimal Threshold Configurations
├── ASQD_2.4/                   # ASQD 2.4 Benchmark & 12,000 Blind Test Datasets
├── tests/                      # 23 Unit & Integration Tests
├── validation/                 # Empirical Research & Analysis Validation Scripts
└── server.py                   # FastAPI REST & WebSocket Streaming Server
```

---

## 📜 License & Citation

Developed for **Smart India Hackathon 2026 — ISRO Problem Statement #26170**.  
Distributed under the MIT License.
