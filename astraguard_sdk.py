"""
AstraGuard 2.0 — Standard ATE SDK Client Module (M1 Contract Frozen)
=======================================================================
Provides standardized input/output contract for Automated Test Equipment (ATE)
and STDF/CSV ingestion interfaces.
"""

import time
import requests
import json
import pandas as pd
from typing import Dict, Any, Generator, List, Optional

class AstraGuardATESDK:
    """
    Official SDK Interface for ISRO ATE Chamber Integration.
    Encapsulates raw ATE measurement structures and communicates with AstraGuard Engine.
    """
    def __init__(self, base_url: str = "http://127.0.0.1:8000", instrument_id: str = "ISRO_ATE_CHAMBER_01", lot_id: str = "LOT_2026_07"):
        self.base_url = base_url.rstrip('/')
        self.instrument_id = instrument_id
        self.lot_id = lot_id

    def check_connection(self) -> bool:
        """Verifies active connectivity to the AstraGuard Backend Server."""
        try:
            res = requests.get(f"{self.base_url}/docs", timeout=3)
            return res.status_code == 200
        except Exception:
            return False

    def submit_measurement(self, component_id: str, measurements: Dict[str, float], wafer_x: float = 0.0, wafer_y: float = 0.0) -> Dict[str, Any]:
        """
        M1 Frozen Contract: Submit parametric measurement dictionary.
        
        Input:
            component_id: str
            measurements: {"iddq_0h": float, "iddq_24h": float, ...}
            wafer_x, wafer_y: float (optional spatial coords)
            
        Output:
            {
               "component_id": str,
               "predicted_168h_iddq_ua": float,
               "anomaly_score": float,
               "risk_tier": "GREEN_AUTO_PASS" | "YELLOW_EXTENDED_TEST" | "RED_EARLY_REJECT",
               "failure_pattern": str,
               "explanation": str,
               "recommended_action": str
            }
        """
        iddq_0h = float(measurements.get("iddq_0h", 0.0))
        iddq_24h = float(measurements.get("iddq_24h", 0.0))
        
        payload = {
            "component_id": str(component_id),
            "iddq_0h": iddq_0h,
            "iddq_24h": iddq_24h,
            "wafer_x": float(wafer_x),
            "wafer_y": float(wafer_y)
        }
        
        res = requests.post(f"{self.base_url}/api/v1/stage-a/predict-single", json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            data["iddq_0h"] = iddq_0h
            data["iddq_24h"] = iddq_24h
            return data
        else:
            raise RuntimeError(f"HTTP Error {res.status_code}: {res.text}")

    def stream_lot_csv(self, csv_filepath: str, interval_sec: float = 0.1, max_records: int = 10) -> Generator[Dict[str, Any], None, None]:
        """Simulates real-time chamber testing by reading and streaming ATE data line-by-line."""
        df = pd.read_csv(csv_filepath)
        if max_records > 0:
            df = df.head(max_records)
            
        for _, row in df.iterrows():
            measurements = {
                "iddq_0h": row["iddq_0h"],
                "iddq_24h": row["iddq_24h"]
            }
            result = self.submit_measurement(
                component_id=row["component_id"],
                measurements=measurements,
                wafer_x=row.get("wafer_x", 0.0),
                wafer_y=row.get("wafer_y", 0.0)
            )
            yield result
            time.sleep(interval_sec)

if __name__ == "__main__":
    print("==================================================")
    print("   ASTRAGUARD 2.0 ATE SDK CLIENT (M1 CONTRACT)    ")
    print("==================================================")
    sdk = AstraGuardATESDK()
    print(f"Connecting to AstraGuard Backend at: {sdk.base_url}")
    if sdk.check_connection():
        print("Status: 🟢 Connected to AstraGuard Engine\n")
    else:
        print("Status: 🔴 Server not reachable! Ensure server.py is running on port 8000.\n")
