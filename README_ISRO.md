<div align="center">

# 🛰️ AstraGuard (ISRO Latent Defect Sentinel)
### Predictive Machine Learning Framework for Electronic Component Burn-In Anomaly & Drift Screening

*Eliminating latent electronic defects in space mission payloads using Dynamic Part Average Testing (dPAT), Time-Series Drift Forecasting, and Explainable AI (XAI).*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=black)](https://scikit-learn.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SHAP](https://img.shields.io/badge/SHAP-XAI-blueviolet?style=for-the-badge)](https://shap.readthedocs.io)
[![SIH 2026](https://img.shields.io/badge/SIH_2026-ISRO-blue?style=for-the-badge)](https://sih.gov.in)

---

**Built for Smart India Hackathon 2026 | Organization: Indian Space Research Organisation (ISRO)**

</div>

---

## 📖 Table of Contents

- [🧠 For Everyone — What Is This?](#-for-everyone--what-is-this)
- [🚨 The Problem: Why Microchips Fail in Space](#-the-problem-why-microchips-fail-in-space)
- [💡 Our Solution — The Simple Version](#-our-solution--the-simple-version)
- [⚙️ For Engineers — System Architecture](#️-for-engineers--system-architecture)
- [🔬 Core Modules Breakdown](#-core-modules-breakdown)
- [📊 Research-Backed Limitations & Solutions](#-research-backed-limitations--solutions)
- [📈 Benchmarks & Metrics](#-benchmarks--metrics)
- [🚀 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [👥 Team](#-team)

---

## 🧠 For Everyone — What Is This?

> **No semiconductor background? Start here. This section breaks it down simply.**

### The Story: The "Trojan Horse" Microchip

Before ISRO launches a satellite like Chandrayaan or Gaganyaan, every single electronic component (microchip, resistor, transistor) undergoes a **Burn-In Test**. 

This means heating the chips to **125°C** while running electricity through them for **168 hours (7 days)**. The goal is to stress-test them on Earth so they don't break in space.

Currently, engineers use **static rules** (like a pass mark on an exam):
- *"If leakage current is below 50 µA, PASS."*

#### The Flaw in Static Limits ❌
Imagine a batch of 1,000 chips. 999 chips have a tiny leakage current of **10 µA**. 
One chip has **45 µA**. 
Technically, 45 µA is below 50 µA, so the old system marks it **PASS**.

**However, that 45 µA chip is an IMPOSTOR.** It has a hidden structural defect. In the vacuum of space, after 6 months of cosmic radiation, that 45 µA chip will suddenly short-circuit, leading to a catastrophic **satellite failure**.

### The AstraGuard Solution 🛡️
AstraGuard replaces static "pass mark" rules with **Dynamic AI Screening**:
1. **Module A (Dynamic Outlier Detection):** Flags chips that are abnormal *relative to their own manufacturing batch*, even if they pass official static limits.
2. **Module B (168h Drift Predictor):** Uses early test data (from 0h and 24h) to **forecast how the chip will behave at 168h**, predicting failures before wasting 7 days of test chamber time.
3. **Module C (QA Inspector Dashboard):** Explains *why* a chip was flagged in plain English so ISRO quality control inspectors can trust and verify the AI decision.

---

## 🚨 The Problem: Why Microchips Fail in Space

In nanometer semiconductor fabrication, subtle flaws like **gate oxide breakdown**, **electromigration**, or **contaminant trapping** create **Latent Defects**.

```
  MANUFACTURING FAULT         INITIAL BENCH TEST (0h)         IN-SPACE OPERATION (Month 6)
┌──────────────────────┐     ┌──────────────────────┐        ┌──────────────────────┐
│ Microscopic oxide    │ ──▶ │ Static test: 45 µA   │  ───▶  │ Thermal runaway!     │
│ crack during wafer   │     │ (Datasheet Limit: 50)│ (Space)│ Satellite goes dark. │
│ etching              │     │ Result: PASSED ❌    │        │ Mission Failed. 💥   │
└──────────────────────┘     └──────────────────────┘        └──────────────────────┘
```

### Key Industry Challenges
1. **Catastrophic Cost of False Negatives:** In space missions, missing **one defective component** (False Negative) can ruin a ₹1,000 Crore mission.
2. **High Cost of Burn-In Testing:** Running 168-hour thermal chambers consumes immense power and delays satellite assembly timelines.
3. **Sub-Micron Intrinsic Leakage Noise:** As transistors get smaller, normal background noise increases, making subtle defect signals harder to detect manually.

---

## 💡 Our Solution — The Simple Version

AstraGuard acts as an **AI Quality Inspector** for space-grade electronics.

```
       TEST DATA (0h, 24h)
    [Iddq, Leakage, Delay]
              │
              ▼
    ┌──────────────────┐
    │    AstraGuard    │
    │    AI Engine     │
    └─────────┬────────┘
              │
      ┌───────┴─────────────────────────────────────────────┐
      ▼                                                     ▼
┌───────────────────────────┐                 ┌───────────────────────────┐
│ Module A: Outlier Detector│                 │ Module B: Drift Predictor │
│ "This chip is 4.2x higher │                 │ "Predicts 168h leakage    │
│ than batch average!"      │                 │ will breach safety slope" │
└─────────────┬─────────────┘                 └─────────────┬─────────────┘
              │                                             │
              └──────────────────────┬──────────────────────┘
                                     ▼
                      ┌─────────────────────────────┐
                      │ Module C: Explainable UI    │
                      │ 🚨 REJECT (Risk Score 94%) │
                      │ SHAP Plot: High 24h Iddq    │
                      └─────────────────────────────┘
```

---

## ⚙️ For Engineers — System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             ASTRAGUARD TECHNICAL ARCHITECTURE                             │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────┐
  │ Parametric Dataset (CSV) │ ← Time-series measurements: Iddq, Leakage, Prop. Delay
  │ (0h, 24h, 96h, 168h)     │   at lot/wafer level
  └────────────┬─────────────┘
               │
               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                       PREPROCESSING & HARMONIZATION ENGINE                          │
  │  • Robust scaling (Median/IQR) per Lot ID                                          │
  │  • Feature engineering: ΔIddq(24h - 0h), Relative Drift Rate S_24                     │
  │  • Missing value imputation (KNN Imputer)                                           │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
            ▼                                     ▼
  ┌───────────────────────────────┐     ┌───────────────────────────────┐
  │   MODULE A: DYNAMIC OUTLIER   │     │  MODULE B: TIME-SERIES DRIFT  │
  │           DETECTOR            │     │           PREDICTOR           │
  ├───────────────────────────────┤     ├───────────────────────────────┤
  │ 1. Dynamic Part Average       │     │ 1. Features: V_0h, V_24h,     │
  │    Testing (dPAT - 3σ / IQR)  │     │    ΔV_24h, Lot_Mean_0h        │
  │ 2. Isolation Forest           │     │ 2. Model: LightGBM / Ridge /  │
  │ 3. Deep Autoencoder           │     │    Temporal Convolution Net   │
  │    (Reconstruction Error > τ) │     │ 3. Output: Forecast V_168h    │
  │                               │     │ 4. Slope Safety Rule:         │
  │ Output: Outlier Score [0 - 1] │     │    S_168 > S_crit → FLAG     │
  └───────────────┬───────────────┘     └───────────────┬───────────────┘
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │ Predictions & Anomaly Scores
                                     ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                        MODULE C: EXPLAINABILITY & AUDIT ENGINE                      │
  │  • SHAP (SHapley Additive exPlanations) Kernel / TreeExplainer                      │
  │  • Human-readable summary: "Flagged because 24h Iddq drift (+35%) exceeds lot trend" │
  │  • Fast-Reject Trigger: Skip remaining 144h burn-in if predicted failure > 95%      │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                           INSPECTOR DASHBOARD (React + FastAPI)                     │
  │  • Single-component inspection cards  • Lot-level distribution histograms           │
  │  • SHAP force plots                   • Automated PDF Audit Report Generation       │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Core Modules Breakdown

### Module A — Dynamic Part Average Testing (dPAT) & Outlier Engine

Standard static limits use global limits (e.g., $I_{leak} \le 50\,\mu\text{A}$). **dPAT calculates dynamic thresholds per manufacturing lot**:

$$\text{Upper Limit} = \mu_{\text{lot}} + k \cdot \sigma_{\text{lot}}$$

Where $k$ is dynamically tuned (typically $k=3$ for $3\sigma$ screening, or $1.5 \times \text{IQR}$ for non-Gaussian parametric distributions).

```python
import numpy as np
from sklearn.ensemble import IsolationForest

class DynamicOutlierDetector:
    def __init__(self, k_sigma: float = 3.0, contamination: float = 0.05):
        self.k_sigma = k_sigma
        self.iso_forest = IsolationForest(contamination=contamination, random_state=42)

    def fit_predict_lot(self, df_lot, feature_col: str):
        # 1. Statistical dPAT
        mean = df_lot[feature_col].mean()
        std = df_lot[feature_col].std()
        upper_bound = mean + (self.k_sigma * std)
        lower_bound = mean - (self.k_sigma * std)
        
        stat_outliers = (df_lot[feature_col] > upper_bound) | (df_lot[feature_col] < lower_bound)
        
        # 2. Machine Learning Isolation Forest (Multivariate)
        ml_scores = self.iso_forest.fit_predict(df_lot[[feature_col]])
        ml_outliers = ml_scores == -1
        
        # Ensemble decision: Flag if either statistical dPAT OR ML flags it
        final_flags = stat_outliers | ml_outliers
        return final_flags, upper_bound
```

---

### Module B — Time-Series Drift Predictor ($0\text{h}, 24\text{h} \rightarrow 168\text{h}$)

Instead of waiting for the full 168 hours of burn-in testing, Module B forecasts $V_{168\text{h}}$ at the 24-hour mark:

$$\hat{V}_{168\text{h}} = f(V_{0\text{h}}, V_{24h}, \Delta V_{24\text{h}-0\text{h}}, \mu_{\text{lot}})$$

$$\text{Predicted Safety Slope } S_{\text{pred}} = \frac{\hat{V}_{168\text{h}} - V_{0\text{h}}}{168}$$

If $S_{\text{pred}} > S_{\text{critical}}$, the component is flagged for **Early Rejection at 24h**, saving **144 hours of test chamber time per batch**.

```python
import lightgbm as lgb
import numpy as np

class DriftPredictor:
    def __init__(self):
        self.model = lgb.LGBMRegressor(
            n_estimators=200,
            learning_rate=0.03,
            max_depth=5,
            random_state=42
        )

    def train(self, X_train, y_train_168h):
        # X_train features: [V_0h, V_24h, delta_24_0, lot_mean_0h, lot_std_0h]
        self.model.fit(X_train, y_train_168h)

    def predict_and_screen(self, X_test, v0_col_idx: int, safety_slope_limit: float):
        v168_pred = self.model.predict(X_test)
        v0_vals = X_test[:, v0_col_idx]
        
        # Calculate predicted drift slope
        pred_slope = (v168_pred - v0_vals) / 168.0
        early_reject_flags = pred_slope > safety_slope_limit
        
        return v168_pred, pred_slope, early_reject_flags
```

---

### Module C — Explainable AI (XAI) for Quality Assurance

Space quality inspectors **will not trust a black box**. Module C uses **SHAP** (SHapley Additive exPlanations) to break down every rejection into human-understandable audit logs.

```python
import shap

def explain_rejection(model, X_sample, feature_names):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    # Generate human-readable narrative
    top_feature_idx = np.argmax(np.abs(shap_values[0]))
    top_feature_name = feature_names[top_feature_idx]
    contribution = shap_values[0][top_feature_idx]
    
    explanation = f"Flagged primarily due to anomalous '{top_feature_name}' " \
                  f"which elevated risk score by {contribution:+.2f} units."
    return explanation, shap_values
```

---

## 📊 Research-Backed Limitations & Solutions

Every machine learning paper in semiconductor test engineering (IEEE / MDPI / ACM) highlights key hurdles. Here is how AstraGuard addresses them:

| Challenge / Limitation | Research Basis | AstraGuard Solution |
|------------------------|----------------|---------------------|
| **Imbalanced Defect Rates** (<0.5% components fail in space-grade lots) | Extreme class imbalance causes standard ML classifiers to over-predict "Pass". | Use **unsupervised anomaly detection** (Isolation Forests, Autoencoders, dPAT) trained on healthy patterns, plus **SMOTE-Tomek** for regression drift boundaries. |
| **Non-Gaussian Parametric Distributions** | Wafer edge components naturally drift differently than center components (bimodal/skewed). | Standard $3\sigma$ fails on non-Gaussian data. AstraGuard uses **IQR-based Boxplot Limits ($1.5 \times \text{IQR}$)** and **Kernel Density Estimation (KDE)**. |
| **High Cost of False Negatives** | Passing a single bad chip (False Negative) can destroy a satellite. | Objective function is tuned with a **custom asymmetric loss function** that penalizes False Negatives 10× more heavily than False Positives. |
| **Thermal Runaway Noise** | Temperature fluctuations in 125°C chambers cause temporary measurement noise. | Apply **Kalman filtering / Moving Average smoothing** across initial time steps to separate true component drift from chamber environmental noise. |
| **Black-Box AI Trust Issue** | ISRO QA inspectors cannot sign off on an unexplained neural network output. | Integrate **SHAP / LIME Force Plots** directly into the QA inspector web dashboard for audit compliance. |

---

## 📈 Benchmarks & Metrics

### Key Metric Formulations

1. **Mean Absolute Error (MAE) for 168h Drift Prediction:**
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} \left| V_{168\text{h, actual}}^{(i)} - \hat{V}_{168\text{h, predicted}}^{(i)} \right|$$

2. **Custom Cost-Weighted Loss (Prioritizing Zero Missed Failures):**
$$\text{Loss} = w_{\text{FN}} \cdot \text{False Negatives} + w_{\text{FP}} \cdot \text{False Positives} \quad (w_{\text{FN}} = 10, w_{\text{FP}} = 1)$$

3. **Time-Saved Metric (Early Rejection Efficiency):**
$$\text{Hours Saved} = N_{\text{early\_rejected}} \times (168\text{h} - 24\text{h}) = N_{\text{early\_rejected}} \times 144\text{ hours}$$

---

## 🚀 Getting Started

### Quick Start (Docker)

```bash
# 1. Clone repo
git clone https://github.com/your-team/astraguard.git
cd astraguard

# 2. Run backend & dashboard
docker compose up -d

# 3. Access Inspector UI at http://localhost:3000
```

### Manual Setup

```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run synthetic data generator (for testing)
python scripts/generate_burnin_data.py --samples 5000 --lots 20

# Run evaluation pipeline
python main.py --data data/burnin_test_data.csv --k-sigma 3.0
```

---

## 📁 Project Structure

```
astraguard/
│
├── 📁 data/                        # Datasets & synthetic generators
│   └── generate_burnin_data.py     # Simulates 0h, 24h, 96h, 168h burn-in data
│
├── 📁 engine/                      # Core Analytics
│   ├── dpat_outlier.py             # Module A: Dynamic Part Average Testing
│   ├── drift_predictor.py          # Module B: 168h Drift Regressor (LightGBM/LSTM)
│   ├── explainability.py          # Module C: SHAP / LIME audit generator
│   └── preprocessing.py            # Robust Scaler & Lot Normalizer
│
├── 📁 app/                         # FastAPI Backend
│   ├── main.py                     # API Entrypoint
│   └── routes/                     # REST Endpoints (/predict, /inspect, /report)
│
├── 📁 frontend/                    # React QA Inspector Dashboard
│   ├── src/components/
│   │   ├── LotDistributionChart.tsx
│   │   ├── ShapForcePlot.tsx
│   │   └── InspectorCard.tsx
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 👥 Team

**AstraGuard** — Built for Smart India Hackathon 2026

| Member | Role |
|--------|------|
| [Name 1] | ML Lead — Dynamic Outlier & Time-Series Models |
| [Name 2] | Data Engineer — Semiconductor Preprocessing Pipeline |
| [Name 3] | Backend Engineer — FastAPI & SHAP Integration |
| [Name 4] | Frontend Lead — React QA Inspector Dashboard |

---

<div align="center">

**Made with ❤️ for ISRO & Space Reliability Engineering**

</div>
