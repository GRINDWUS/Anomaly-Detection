# 🛡️ AstraGuard 2.0 — Space-Grade Semiconductor & Telemetry Reliability Platform

> **Smart India Hackathon 2026 Submission** | **Problem Statement #SIH26170 (ISRO)**  
> *Physics-Informed Predictive Semiconductor Burn-In & In-Orbit Satellite Telemetry Reliability Platform*

---

## 📖 System Architecture & Core Highlights

AstraGuard 2.0 is an end-to-end reliability platform engineered specifically for space-grade microelectronics qualification and satellite in-orbit telemetry monitoring.

```text
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ASTRAGUARD 2.0 SYSTEM ARCHITECTURE                    │
 └─────────────────────────────────────────────────────────────────────────┘

   [ASTRAGUARD ATE SDK]  ──(REST/JSON)──▶  [FASTAPI INGESTION ENGINE]
   (pip install astraguard-sdk)             (Port 8000)
            │                                      │
            ▼                                      ▼
   [ATE CHAMBER SIMULATOR]               [MODULE A: OUTLIER DETECTOR]
   (Normal & Injected Fault Streams)       (Dynamic Lot Spatial Z-Score)
                                                   │
                                                   ▼
                                         [MODULE B: DRIFT FORECASTER]
                                         (XGBoost 168h IDDQ Predictor)
                                                   │
                                                   ▼
                                         [3-TIER RISK DECISION ENGINE]
                                         (GREEN / YELLOW / RED Logic)
                                                   │
                                     ┌─────────────┴─────────────┐
                                     ▼                           ▼
                             [WEBSOCKET STREAM]          [SHAP EXPLANATION]
                                     │                           │
                                     └─────────────┬─────────────┘
                                                   ▼
                                     [NEXT.JS OPERATOR DASHBOARD]
                                     (Port 3000 - 4 Live Views)
```

---

## ⚡ Quick Start & Live Demonstration Guide

Follow these steps for a complete offline/online demonstration in front of the panel:

### 1. Environment Setup & SDK Installation
```bash
# Clone repository and enter directory
cd "D:\SIH 2026"

# Install AstraGuard SDK cleanly
pip install -e .
```

### 2. Start the AstraGuard Backend Server
```bash
python server.py
```
*Backend API available at: `http://127.0.0.1:8000` | OpenAPI Docs: `http://127.0.0.1:8000/docs`*

### 3. Launch the Next.js Dashboard
```bash
cd dashboard
npm run dev
```
*Operator Dashboard accessible at: `http://localhost:3000`*

### 4. Run the Live ATE Chamber & Failure Injection Demo
In a separate terminal:
```bash
python ate_chamber_simulator.py
```

---

## 🌐 Testing on Another Machine (Panel / Remote Laptop Setup)

If the ISRO panel asks you to install and test the SDK on **their laptop** or another external machine connected to the same Wi-Fi/LAN network:

### Step 1: Bind your Backend Server to `0.0.0.0`
On host machine running `server.py`, pass your LAN IP or `0.0.0.0`:
```bash
# Finds host machine LAN IP (e.g., 192.168.1.15)
ipconfig
```

### Step 2: Install SDK on the Remote Machine
Copy the pre-compiled wheel package (`dist/astraguard_sdk-2.0.0-py3-none-any.whl`) or git repo to their laptop, then run:
```bash
pip install astraguard_sdk-2.0.0-py3-none-any.whl
```
*(Or install directly via git/network path: `pip install git+https://github.com/your-repo/sih-2026.git`)*

### Step 3: Run SDK Code on the Remote Machine
On the external laptop, run 3 lines of Python to send live ATE measurements to your server:
```python
from astraguard_sdk import AstraGuardATESDK

# Point base_url to your laptop's IP address (e.g. http://192.168.1.15:8000)
sdk = AstraGuardATESDK(base_url="http://<YOUR_HOST_LAPTOP_IP>:8000")

# Verify connection
if sdk.check_connection():
    print("🟢 Connected to Host AstraGuard Server!")

# Send ATE measurement from remote machine
result = sdk.submit_measurement(
    component_id="ISRO_PANEL_TEST_001",
    measurements={"iddq_0h": 12.4, "iddq_24h": 32.1}
)

print("Remote Prediction Result:", result)
# Output: {'component_id': 'ISRO_PANEL_TEST_001', 'predicted_168h_iddq_ua': 1580.4, 'risk_tier': 'RED_EARLY_REJECT'}
```


---

## 🔬 Core System Features

1. **Strict Information Boundary:** Prediction models rely *only* on $0\text{h}$ and $24\text{h}$ ATE measurements to predict $168\text{h}$ leakage, preventing data leakage.
2. **Module A (Dynamic Lot Outlier Detection):** Calculates relative lot spatial z-scores and population drift velocities.
3. **Module B (168h Time-Series Forecast):** Predicts final $168\text{h}$ leakage with **$2.73\,\mu\text{A}$ MAE** and **$0.0\%$ False Negative Rate** on blind test lots.
4. **3-Tier Risk Engine:**
   * 🟢 **GREEN_AUTO_PASS:** Early pass at $24\text{h}$ ($84.69\%$ chamber-hour reduction).
   * 🟡 **YELLOW_EXTENDED_TEST:** Assigned for extended $72\text{h}$ testing.
   * 🔴 **RED_EARLY_REJECT:** Flagged for early QA rejection.
5. **Stage-B Post-Launch Monitoring:** Tracks in-orbit satellite sensor telemetry against pre-launch qualified fingerprints for FDIR early warning.

---

## 🧪 Running Automated Unit & Integration Tests

Execute the comprehensive system test suite:
```bash
python -m unittest discover -s tests
```
*Validates SDK contracts, server API endpoints, SHAP attributions, and Stage-B telemetry functions.*

---
*Created for ISRO SIH 2026 Hackathon Presentation.*
