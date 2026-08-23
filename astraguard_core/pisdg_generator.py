"""
AstraGuard Core - Step 1 & 2: Realistic Physics-Informed Synthetic Data Generator (PISDG)
Calibrated against open NASA microelectronics degradation dynamics.
"""
import numpy as np
import pandas as pd
import os
from typing import Tuple

def generate_ate_lot(
    lot_id: str,
    num_components: int = 1000,
    defect_rate: float = 0.04,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates a realistic ATE parametric dataset for a semiconductor lot.
    Includes:
    - Wafer spatial coordinates (X, Y) with edge thermal bias
    - 0h, 24h, 96h, 168h IDDQ readings
    - Gaussian chamber measurement noise (±0.35 µA)
    - 3 distinct physical failure modes (NBTI Power Law, Electromigration Linear, Thermal Runaway Exponential)
    """
    np.random.seed(random_seed)
    
    # 1. Wafer Spatial Coordinates (Normalized -1.0 to +1.0)
    radius = np.sqrt(np.random.uniform(0, 1, num_components))
    angle = np.random.uniform(0, 2 * np.pi, num_components)
    coord_x = radius * np.cos(angle)
    coord_y = radius * np.sin(angle)
    
    # 2. Baseline 0h IDDQ with edge thermal gradient (dies on perimeter leak slightly more)
    spatial_edge_bias = 4.5 * (coord_x**2 + coord_y**2)
    base_iddq_0h = np.random.normal(loc=12.0, scale=1.8, size=num_components) + spatial_edge_bias
    
    # 3. Inject Ground Truth Defect Labels
    is_defective = np.random.choice([0, 1], size=num_components, p=[1 - defect_rate, defect_rate])
    
    iddq_24h = np.zeros(num_components)
    iddq_96h = np.zeros(num_components)
    iddq_168h = np.zeros(num_components)
    failure_modes = []
    
    for i in range(num_components):
        noise_24 = np.random.normal(0, 0.35)
        noise_96 = np.random.normal(0, 0.35)
        noise_168 = np.random.normal(0, 0.35)
        
        if is_defective[i] == 0:
            # Normal Healthy Aging (Power law n=0.15)
            iddq_24h[i] = base_iddq_0h[i] + 0.7 * (24**0.15) + noise_24
            iddq_96h[i] = base_iddq_0h[i] + 0.7 * (96**0.15) + noise_96
            iddq_168h[i] = base_iddq_0h[i] + 0.7 * (168**0.15) + noise_168
            failure_modes.append("HEALTHY")
        else:
            # Latent Defect: Assign kinetic mode
            mode = np.random.choice(["NBTI_POWER_LAW", "ELECTROMIGRATION_LINEAR", "THERMAL_RUNAWAY_EXP"])
            failure_modes.append(mode)
            
            if mode == "NBTI_POWER_LAW":
                # Oxide trapping: n=0.45 exponent surge
                iddq_24h[i] = base_iddq_0h[i] + 4.2 * (24**0.45) + noise_24
                iddq_96h[i] = base_iddq_0h[i] + 4.2 * (96**0.45) + noise_96
                iddq_168h[i] = base_iddq_0h[i] + 4.2 * (168**0.45) + noise_168
            elif mode == "ELECTROMIGRATION_LINEAR":
                # Linear current drift
                iddq_24h[i] = base_iddq_0h[i] + 0.85 * 24 + noise_24
                iddq_96h[i] = base_iddq_0h[i] + 0.85 * 96 + noise_96
                iddq_168h[i] = base_iddq_0h[i] + 0.85 * 168 + noise_168
            elif mode == "THERMAL_RUNAWAY_EXP":
                # Exponential breakdown
                iddq_24h[i] = base_iddq_0h[i] * np.exp(0.028 * 24) + noise_24
                iddq_96h[i] = base_iddq_0h[i] * np.exp(0.028 * 96) + noise_96
                iddq_168h[i] = base_iddq_0h[i] * np.exp(0.028 * 168) + noise_168

    df = pd.DataFrame({
        "lot_id": lot_id,
        "component_id": [f"{lot_id}_COMP_{i:04d}" for i in range(num_components)],
        "wafer_x": np.round(coord_x, 4),
        "wafer_y": np.round(coord_y, 4),
        "iddq_0h": np.round(base_iddq_0h, 2),
        "iddq_24h": np.round(iddq_24h, 2),
        "iddq_96h": np.round(iddq_96h, 2),
        "iddq_168h_actual": np.round(iddq_168h, 2),
        "is_defective_gt": is_defective,
        "failure_mode_gt": failure_modes
    })
    return df

if __name__ == "__main__":
    os.makedirs("D:\\SIH 2026\\astraguard_core\\data", exist_ok=True)
    # Generate 5 Training Lots and 2 Validation Lots
    for lot_idx in range(1, 8):
        lot_name = f"LOT_2026_{lot_idx:02d}"
        lot_df = generate_ate_lot(lot_id=lot_name, random_seed=40 + lot_idx)
        filepath = f"D:\\SIH 2026\\astraguard_core\\data\\{lot_name}.csv"
        lot_df.to_csv(filepath, index=False)
        print(f"Saved dataset: {filepath} ({len(lot_df)} rows)")
