# 🧊 Software Requirements Specification (SRS)
## PolarNav-AI: Antarctic Sea-Ice, Iceberg Trajectory, and Navigation Decision Support System

---

## 📄 Executive Summary (The Layman's Analogy)

Imagine driving a ₹500 Crore ship through an ocean filled with floating blue ice boulders, foggy darkness, and shifting ice sheets. 
Currently, ship captains in Antarctica look at **yesterday's satellite map** (which is already outdated) and use binoculars. If the ship gets trapped in 10-foot-thick ice, it costs lakhs of rupees per day in fuel, delays scientific missions, or worse, risks vessel damage.

**PolarNav-AI** acts like a **Google Maps for Polar Ships**. 
- It uses **radar satellite eyes** that see through Antarctic night and clouds.
- It uses **AI prediction** to forecast where icebergs will drift 3 days into the future.
- It calculates the **fastest, safest, and most fuel-efficient route** around ice obstacles in real-time.

---

## 1. 📌 Introduction & Scope

### 1.1 Objective
To develop an AI/ML-driven decision support system for **NCPOR (National Centre for Polar and Ocean Research)** to guide Indian research vessels (like *ORV Sagar Nidhi*) through the Southern Ocean to Indian Antarctic stations (**Maitri** and **Bharti**).

### 1.2 User Roles & Operational Environment
- **Primary User:** Ship Captain & Polar Navigation Officers aboard research vessels.
- **Secondary User:** NCPOR Mission Control in Goa (monitoring ship fleet status).
- **Environment:** Low-bandwidth satellite links at sea, sub-zero conditions, 24-hour polar winter darkness.

---

## 2. 🏗️ System Architecture & Key Factors

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            POLARNAV-AI DATA FLOW                                 │
└──────────────────────────────────────────────────────────────────────────────────┘

  [Sentinel-1 SAR Radar]     [NSIDC Sea-Ice Conc]     [CMEMS Currents & ERA5 Winds]
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│       MODULE 1        │ │       MODULE 2        │ │       MODULE 3        │
│  Ice & Iceberg Detect │ │   Drift Predictor     │ │   Route Optimizer     │
│   (U-Net + OpenCV)    │ │ (ConvLSTM + Physics)  │ │(Cost-Grid Dynamic A*) │
└───────────┬───────────┘ └───────────┬───────────┘ └───────────┬───────────┘
            │                         │                         │
            └─────────────────────────┼─────────────────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │   SHIP NAVIGATION PANEL   │
                        │ (Offline React/Leaflet UI)│
                        └───────────────────────────┘
```

---

## 3. 🔬 Deep-Dive: System Modules & Engineering Design

### Module 1: Satellite Iceberg & Sea-Ice Detection Engine
* **Input:** Sentinel-1 C-band Synthetic Aperture Radar (SAR) Dual-Pol ($HH + HV$) images.
* **Why SAR?** Optical cameras are useless during 6 months of Antarctic polar night or thick clouds. Radar waves penetrate darkness and clouds!
* **Model Architecture:** **U-Net / ResNet-50 Encoder** fine-tuned on polar SAR benchmark data.
* **Layman Analogy:** Like putting night-vision goggles on the ship that highlight icebergs in red and clear water in green.

### Module 2: Iceberg & Sea-Ice Trajectory Forecasting (24h - 72h)
* **Input:** Historical ice movement + CMEMS Ocean Surface Currents ($U, V$) + ERA5 Surface Winds ($U_{10}, V_{10}$).
* **Mathematical Drift Equation (Lagrangian Kinematic Equation):**
$$\vec{V}_{\text{iceberg}} = \alpha \cdot \vec{V}_{\text{wind}} + \beta \cdot \vec{V}_{\text{ocean\_current}} + \vec{F}_{\text{Coriolis}}$$
Where $\alpha \approx 0.02$ (2% wind drag) and $\beta \approx 0.8$ (80% water drag).
* **AI Model:** **ConvLSTM (Convolutional Long Short-Term Memory)** to predict non-linear sea-ice concentration changes ($SIC$) for the next 72 hours.
* **Layman Analogy:** If you drop a leaf in a flowing river on a windy day, where will it be in 3 hours? We calculate that for 1,000-ton icebergs!

### Module 3: Dynamic Ice-Aware Route Optimizer
* **Input:** Predicted Sea-Ice Concentration Grid + Iceberg Danger Polygons + Ship Fuel Characteristics.
* **Algorithm:** **Dynamic A* / Fast Marching Method (FMM)** on a 2D Risk Cost Grid.
* **Cost Function:**
$$\text{Cell Cost} = w_1 \cdot \text{Distance} + w_2 \cdot (\text{SeaIce\_Density})^2 + w_3 \cdot \frac{1}{\text{Dist\_to\_Iceberg}}$$
* **Layman Analogy:** Google Maps recalculating your route when it detects a traffic jam ahead — except here, the traffic jam is a 10-mile pack of sea ice!

---

## ⚠️ 4. Key Problems, Real-World Limitations & Research Solutions

Here are the **6 biggest challenges** you will face on this project, supported by academic research papers, along with our concrete solutions:

---

### 🔴 Problem #1: "Polar Night & Cloud Cover" (Optical Satellites Don't Work)
* **The Challenge:** Antarctica experiences 24-hour pitch darkness during polar winter. Optical satellites (like Sentinel-2 or Landsat) produce 100% black images.
* **Research Paper Context:** *IEEE TGRS (Transactions on Geoscience and Remote Sensing)* papers show optical satellite availability drops to $<15\%$ in high latitudes.
* **Our Solution (Layman Explanation):** 
  - **Solution:** We strictly use **SAR (Synthetic Aperture Radar)**. 
  - **Layman Analogy:** Sound waves/sonar in a dark room. Radar sends its own radio waves down to Earth and listens for the bounce. Ice reflects radio waves differently than liquid ocean water, making icebergs shine bright white even in zero daylight.

---

### 🔴 Problem #2: "Speckle Noise in Radar Imagery" (False Iceberg Alarms)
* **The Challenge:** SAR radar images suffer from "speckle noise" — graininess caused by ocean wave ripples that look identical to small icebergs.
* **Research Paper Context:** *MDPI Remote Sensing (2024)* highlights that ocean wave roughness leads to high false-positive rates in automated iceberg detectors.
* **Our Solution:**
  - **Solution:** Apply a **Lee Speckle Filter** followed by **Dual-Polarization Ratio Thresholding ($HH / HV$)**. Icebergs depolarize radar signals differently than ocean waves.

---

### 🔴 Problem #3: "Low Bandwidth Internet at Sea" (Can't Download Gigabytes of Data)
* **The Challenge:** Ships near Antarctica communicate via slow Iridium satellite links (often $<100\text{ kbps}$). You CANNOT stream a 2GB satellite image to the ship.
* **Our Solution (Layman Explanation):**
  - **Solution:** **Edge Computing Strategy.** The heavy AI processing runs on cloud servers in India. The cloud server converts the massive 2GB image into a tiny **Vector GeoJSON Route File (less than 50 KB)**.
  - **Layman Analogy:** Instead of downloading a high-definition video of a road map, the ship just receives a text message with GPS turn-by-turn coordinates!

---

### 🔴 Problem #4: "Non-Linear Iceberg Drift" (Wind vs. Water Drag Conflict)
* **The Challenge:** Deep icebergs with deep underwater "keels" move with ocean currents, while flat ice floes move with surface winds. Simple linear drift prediction fails.
* **Research Paper Context:** *The Cryosphere (Copernicus 2023)* demonstrates that uncoupled drift models accumulate over 30 km of trajectory error within 48 hours.
* **Our Solution:**
  - **Solution:** Use a **Hybrid Physics-Informed Neural Network (PINN)**. We combine physical hydrodynamics equations with a ConvLSTM ML model so physical laws constrain the AI's spatial predictions.

---

### 🔴 Problem #5: "Sharp Sharp Turns" (Ships Can't Turn Like Cars)
* **The Challenge:** Standard grid pathfinding (like basic A*) produces sharp 90-degree zig-zag turns that a 10,000-ton research ship physically cannot make in sea ice.
* **Our Solution:**
  - **Solution:** Use **Dubins Path / Fast Marching Method (FMM)** which incorporates the ship's minimum turning radius and momentum constraints.

---

### 🔴 Problem #6: "Changing Ice Conditions During Voyage" (Dynamic Environment)
* **The Challenge:** A route calculated at 8:00 AM might be blocked by 2:00 PM because ice shifts with ocean tides.
* **Our Solution:**
  - **Solution:** **Anytime Repairing A* (ARA*) Algorithm.** The system continuously runs low-overhead spatial checks against updated SAR streams and recalculates alternate waypoints on the fly.

---

## 📊 5. Non-Functional Requirements & Performance Benchmarks

| Metric | Target Goal | Justification |
|--------|-------------|---------------|
| **Iceberg Segmentation Accuracy (IoU)** | $> 85\%$ | Prevents missing hazardous ice floes |
| **72h Trajectory Mean Error** | $< 8 \text{ km}$ | Keeps vessel safely outside iceberg danger buffer |
| **Payload Size sent to Ship** | $< 100 \text{ KB}$ | Works on slow satellite links |
| **Path Optimization Time** | $< 15 \text{ seconds}$ | Instant routing response for ship captain |
| **Fuel Savings** | $12\% - 18\%$ | Saves lakhs of rupees in diesel consumption |

---

## 🚀 6. System Implementation Roadmap (36-Hour Hackathon Strategy)

```
HOUR 0 - 12: DATA & SEGMENTATION
├── Download pre-processed Sentinel-1 SAR samples (Prydz Bay / Maitri Corridor)
├── Run Lee Filter & train U-Net model on Kaggle Statoil SAR iceberg dataset
└── Output: Binary Ice/Water Probability Grid

HOUR 12 - 24: TRAJECTORY & PATHFINDING
├── Build Kinematic Drift model (incorporating ERA5 U/V vectors)
├── Implement Dynamic A* on 2D Sea-Ice Cost Grid
└── Output: Optimized Waypoint Array [Lat, Lon]

HOUR 24 - 36: DASHBOARD & PRESENTATION
├── Build Leaflet/Streamlit UI with satellite layer & ship route overlay
├── Prepare live demo showing simulated iceberg drift & route recalculation
└── Final pitch deck creation targeting NCPOR judges
```

---

<div align="center">

**Prepared for Smart India Hackathon 2026 | NCPOR & Ministry of Earth Sciences**

</div>
