"""
AstraGuard Core - Step 3, 4 & 5: Baseline Evaluator, 168h Predictor & 3-Tier Risk Engine (Fast Version)
Uses spatial wafer coordinate polynomial residual features instead of GPR for fast training/inference.
"""
import numpy as np
import pandas as pd
import xgboost as xgb
from typing import Dict, Any

class AstraGuardPredictorFast:
    def __init__(self, failure_threshold_168h: float = 45.0):
        self.failure_threshold_168h = failure_threshold_168h
        self.xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            random_state=42,
            n_jobs=-1
        )
        self.is_trained = False

    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts temporal drift and spatial polynomial features fast."""
        feats = pd.DataFrame()
        feats["iddq_0h"] = df["iddq_0h"]
        feats["iddq_24h"] = df["iddq_24h"]
        feats["delta_24h"] = df["iddq_24h"] - df["iddq_0h"]
        feats["drift_rate_24h"] = feats["delta_24h"] / 24.0
        feats["drift_acceleration"] = feats["delta_24h"] / (df["iddq_0h"] + 1e-5)
        
        # Spatial polynomial features (dist from wafer center)
        dist_from_center = np.sqrt(df["wafer_x"]**2 + df["wafer_y"]**2)
        feats["dist_from_center"] = dist_from_center
        
        # Robust spatial Z-score approximation
        lot_mean_0h = df["iddq_0h"].mean()
        lot_std_0h = df["iddq_0h"].std() + 1e-5
        feats["spatial_z_score"] = (df["iddq_0h"] - lot_mean_0h) / lot_std_0h
        return feats

    def fit(self, train_df: pd.DataFrame):
        X_train = self._extract_features(train_df)
        y_train = train_df["iddq_168h_actual"]
        self.xgb_model.fit(X_train, y_train)
        self.is_trained = True

    def predict_lot(self, test_df: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise ValueError("Model is not trained! Call fit() first.")
            
        X_test = self._extract_features(test_df)
        pred_168h = self.xgb_model.predict(X_test)
        
        result_df = test_df.copy()
        result_df["predicted_168h_iddq"] = np.round(pred_168h, 2)
        result_df["spatial_z_score"] = np.round(X_test["spatial_z_score"], 2)
        result_df["delta_24h"] = np.round(X_test["delta_24h"], 2)
        
        tiers = []
        for idx, row in result_df.iterrows():
            pred = row["predicted_168h_iddq"]
            z_score = abs(row["spatial_z_score"])
            drift = row["delta_24h"]
            
            if pred > self.failure_threshold_168h or z_score > 3.2 or drift > 12.0:
                tiers.append("RED_EARLY_REJECT")
            elif pred > (self.failure_threshold_168h * 0.75) or z_score > 2.0 or drift > 5.0:
                tiers.append("YELLOW_EXTENDED_TEST")
            else:
                tiers.append("GREEN_AUTO_PASS")
                
        result_df["risk_tier"] = tiers
        return result_df
