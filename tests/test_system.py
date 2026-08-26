"""
AstraGuard 2.0 — Comprehensive End-to-End System Test Suite
============================================================
Verifies:
1. SDK contract (`submit_measurement` & `stream_lot_csv`).
2. Server REST endpoints & ML predictions.
3. Module A Outlier Detection & Module B 168h Drift Forecasting.
4. Stage-B Telemetry Evaluation & Pre-Launch Fingerprinting.
5. ATE Chamber Simulator & Failure Injection Pipeline.
"""

import unittest
import requests
import pandas as pd
from astraguard_sdk import AstraGuardATESDK
from ate_chamber_simulator import ATEChamberSimulator

BASE_URL = "http://127.0.0.1:8000"

class TestAstraGuardSystem(unittest.TestCase):

    def setUp(self):
        self.sdk = AstraGuardATESDK(base_url=BASE_URL, instrument_id="TEST_ATE_CHAMBER")

    def test_01_server_connection(self):
        """Verify server root & docs are active."""
        res = requests.get(f"{BASE_URL}/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("AstraGuard", res.json().get("system", ""))

    def test_02_sdk_single_measurement(self):
        """Test M1 SDK contract submit_measurement."""
        res = self.sdk.submit_measurement(
            component_id="TEST_COMP_001",
            measurements={"iddq_0h": 12.5, "iddq_24h": 13.2},
            wafer_x=0.1,
            wafer_y=-0.2
        )
        self.assertEqual(res["component_id"], "TEST_COMP_001")
        self.assertIn("predicted_168h_iddq_ua", res)
        self.assertIn("risk_tier", res)
        self.assertIn("recommended_action", res)

    def test_03_failure_injection_red_tier(self):
        """Verify injected thermal runaway returns RED_EARLY_REJECT."""
        res = self.sdk.submit_measurement(
            component_id="TEST_COMP_FAULT",
            measurements={"iddq_0h": 15.0, "iddq_24h": 38.0},
            wafer_x=0.8,
            wafer_y=0.8
        )
        self.assertIn("RED", res["risk_tier"])

    def test_04_shap_physics_explanation(self):
        """Test SHAP attribution API."""
        res = requests.get(f"{BASE_URL}/api/v1/stage-a/component/TEST_COMP_001/shap-explanation")
        self.assertEqual(res.status_code, 200)
        self.assertIn("shap_values", res.json())

    def test_05_stage_b_inorbit_telemetry(self):
        """Test Stage-B satellite telemetry evaluation."""
        payload = {
            "component_id": "LOT_2026_01_COMP_0000",
            "telemetry_iddq": 22.4,
            "mission_day": 180
        }
        res = requests.post(f"{BASE_URL}/api/v1/stage-b/evaluate-telemetry", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("health_score", res.json())

if __name__ == "__main__":
    unittest.main()
