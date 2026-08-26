"""
AstraGuard Core — Phase 4 & 5: Outlier Detector (Module A) & Drift Predictor (Module B)
======================================================================================
Strictly maps to ISRO PS #26170 requirements:
  - Module A: Dynamic Lot Outlier Detection (Relative Population Z-Score & Drift Velocity).
  - Module B: Time-Series Drift Predictor (0h + 24h -> Forecasts 168h Value).
  - Risk Engine: Classifies dies into GREEN_AUTO_PASS, YELLOW_EXTENDED_TEST, or RED_EARLY_REJECT.
"""

import numpy as np
import pandas as pd
import xgboost as xgb
from typing import Dict, Any, Tuple

class AstraGuardPredictorFast:
    def __init__(self, failure_threshold_168h: float = 45.0):
        self.failure_threshold_168h = failure_threshold_168h
        self.xgb_model = xgb.XGBRegressor(
            n_estimators=120,
            max_depth=4,
            learning_rate=0.05,
            random_state=42,
            n_jobs=-1
        )
        self.is_trained = False

    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Phase 4: Feature Engineering & Temporal Kinetics
        Extracts temporal drift and spatial polynomial features without data leakage.
        """
        feats = pd.DataFrame()
        feats["iddq_0h"] = df["iddq_0h"]
        feats["iddq_24h"] = df["iddq_24h"]
        
        # Temporal Kinetics
        delta_24h = df["iddq_24h"] - df["iddq_0h"]
        feats["delta_24h"] = delta_24h
        feats["drift_velocity_24h"] = delta_24h / 24.0
        feats["drift_acceleration_rel"] = delta_24h / (df["iddq_0h"] + 1e-5)
        
        # Spatial Wafer Coordinates
        wafer_x = df.get("wafer_x", pd.Series(0.0, index=df.index))
        wafer_y = df.get("wafer_y", pd.Series(0.0, index=df.index))
        feats["dist_from_center"] = np.sqrt(wafer_x**2 + wafer_y**2)
        
        # Module A: Relative Population Spatial Z-Score (Standard Z)
        lot_mean_0h = df["iddq_0h"].mean()
        lot_std_0h = df["iddq_0h"].std() + 1e-5
        feats["spatial_z_score"] = (df["iddq_0h"] - lot_mean_0h) / lot_std_0h
        
        # Robust Population Z-Score (Median + MAD: 1.4826 * MAD)
        lot_median_0h = df["iddq_0h"].median()
        lot_mad_0h = (df["iddq_0h"] - lot_median_0h).abs().median() + 1e-5
        feats["robust_z_score"] = (df["iddq_0h"] - lot_median_0h) / (1.4826 * lot_mad_0h)
        
        # Dynamic 24h Population Drift Outlier Score (Standard & Robust)
        lot_mean_delta = delta_24h.mean()
        lot_std_delta = delta_24h.std() + 1e-5
        feats["drift_z_score"] = (delta_24h - lot_mean_delta) / lot_std_delta
        
        lot_median_delta = delta_24h.median()
        lot_mad_delta = (delta_24h - lot_median_delta).abs().median() + 1e-5
        feats["robust_drift_z_score"] = (delta_24h - lot_median_delta) / (1.4826 * lot_mad_delta)
        
        return feats


    def fit(self, train_df: pd.DataFrame):
        """Train Module B Regressor using 0h and 24h features to predict 168h target."""
        X_train = self._extract_features(train_df)
        y_train = train_df["iddq_168h_actual"]
        self.xgb_model.fit(X_train, y_train)
        self.is_trained = True

    def compute_module_a_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Module A: Dynamic Outlier Detection System
        Flags population anomalies (e.g. 45 µA in a 10 µA lot is flagged even if max limit is 50 µA).
        """
        feats = self._extract_features(df)
        outlier_df = pd.DataFrame(index=df.index)
        outlier_df["component_id"] = df["component_id"]
        outlier_df["spatial_z_score"] = np.round(feats["spatial_z_score"], 2)
        outlier_df["drift_z_score"] = np.round(feats["drift_z_score"], 2)
        outlier_df["is_population_anomaly"] = (abs(feats["spatial_z_score"]) > 3.0) | (abs(feats["drift_z_score"]) > 3.0)
        return outlier_df

    def predict_lot(self, test_df: pd.DataFrame) -> pd.DataFrame:
        """Full Inference Pipeline (Module A Outlier Detection + Module B 168h Drift Forecasting)."""
        if not self.is_trained:
            raise ValueError("Model is not trained! Call fit() first.")
            
        X_test = self._extract_features(test_df)
        pred_168h = self.xgb_model.predict(X_test)
        
        result_df = test_df.copy()
        result_df["predicted_168h_iddq"] = np.round(pred_168h, 2)
        result_df["spatial_z_score"] = np.round(X_test["spatial_z_score"], 2)
        result_df["drift_z_score"] = np.round(X_test["drift_z_score"], 2)
        result_df["delta_24h"] = np.round(X_test["delta_24h"], 2)
        
        # 3-Tier Decision Logic aligned with Space Standards (MIL-STD-883 Method 3005.1 & ESCC 9000)
        # - Red: Critical Failure (Predicted > 40 µA, Z-score > 2.5, Delta_24h > 3.0 µA)
        # - Yellow: Marginal Drift / Statistical Outlier (Predicted > 22 µA, Z-score > 1.6, Delta_24h > 1.2 µA) -> Assigned +48h Extended ESS
        # - Green: High-Reliability Flight Candidate
        tiers = []
        for idx, row in result_df.iterrows():
            pred = row["predicted_168h_iddq"]
            spatial_z = abs(row["spatial_z_score"])
            drift_z = abs(row["drift_z_score"])
            drift_val = row["delta_24h"]
            
            if pred >= 40.0 or spatial_z >= 2.5 or drift_z >= 2.5 or drift_val >= 3.0:
                tiers.append("RED_EARLY_REJECT")
            elif pred >= 22.0 or spatial_z >= 1.6 or drift_z >= 1.6 or drift_val >= 1.2:
                tiers.append("YELLOW_EXTENDED_TEST")
            else:
                tiers.append("GREEN_AUTO_PASS")
                
        result_df["risk_tier"] = tiers
        return result_df

