"""
AstraGuard 2.3 — ASQD Multi-Device Physics Models
===================================================
Provides device-specific parametric drift trajectory generators for:
  - DIGITAL_IC: Arrhenius IDDQ drift (existing, kept identical for PS backward compat)
  - MEMS_GYROSCOPE: Viscoelastic zero-rate-offset drift + stiction risk
  - IMAGE_SENSOR: Shockley-Read-Hall dark current trap generation

Evidence:
  DIGITAL_IC model: [PE] Arrhenius I∝exp(-Ea/kT); Ea=0.68eV from CMOS oxide aging literature.
  MEMS model: [PE] Viscoelastic creep/stress relaxation; ZRO∝log(t) + spring constant drift.
  Image Sensor model: [PE] SRH generation: ni∝exp(-Eg/2kT); dark current doubles ~8-10°C.

Synthetic parameters (populations, noise, spec limits):
  All numerical distributions are [SA] unless otherwise noted.
"""

import numpy as np


# ===========================================================================
# DIGITAL IC — Arrhenius IDDQ Drift (Legacy, PS-compatible, unchanged)
# ===========================================================================
class ArrheniusIDDQModel:
    """[PE] Arrhenius CMOS IDDQ model. Unchanged for PS benchmark backward compat."""
    def __init__(self, base_iddq_uA: float = 1.2, ea_eV: float = 0.68, aging_rate: float = 0.001):
        self.base_iddq = base_iddq_uA
        self.ea = ea_eV
        self.k_boltzmann = 8.617333262145e-5  # eV/K [PE]
        self.aging_rate = aging_rate

    def generate_trajectory(self, num_hours: int = 168, profile: str = "NOMINAL"):
        trajectory = []
        for hour in range(num_hours + 1):
            temp_c = 25.0 + 100.0 * (1.0 - np.exp(-hour / 2.0))
            temp_k = temp_c + 273.15
            arrhenius_factor = np.exp(-self.ea / (self.k_boltzmann * temp_k))
            aging_component = self.aging_rate * hour

            if profile == "NOMINAL":
                iddq = self.base_iddq * (arrhenius_factor + aging_component * 0.5)
            elif profile == "THERMAL_RUNAWAY":
                if hour >= 24:
                    runaway = 0.5 * np.exp(0.04 * (hour - 24))
                    iddq = self.base_iddq * (arrhenius_factor + aging_component) + runaway
                else:
                    iddq = self.base_iddq * (arrhenius_factor + aging_component * 0.5)
            elif profile == "ELECTROMIGRATION":
                accel = 1.0 + (hour / 168.0) ** 2 * 35.0
                iddq = self.base_iddq * (arrhenius_factor + aging_component * accel)
            elif profile == "SPATIAL_OUTLIER":
                iddq = 42.5 * (arrhenius_factor + aging_component * 0.3)
            elif profile == "DIELECTRIC_OSCILLATION":
                osc = 12.5 * np.sin(2 * np.pi * hour / 12.0)
                iddq = self.base_iddq * (arrhenius_factor + aging_component * 0.5) + osc
            else:
                iddq = self.base_iddq * (arrhenius_factor + aging_component * 0.5)

            noise = np.random.normal(0, 0.02)
            iddq = max(0.1, iddq + noise)
            trajectory.append(round(float(iddq), 4))
        return trajectory


# ===========================================================================
# MEMS GYROSCOPE — Viscoelastic ZRO Drift Model
# ===========================================================================
class ViscoelasticMEMSModel:
    """
    [PE] MEMS zero-rate-offset (ZRO) drift model based on viscoelastic
    stress relaxation in die attach and packaging materials.

    ZRO(t) = ZRO_0 + A * (1 - exp(-t/tau)) + B * log(1 + t/t0) + noise
    
    A·(1-exp(-t/τ)): exponential stress relaxation [PE]
    B·log(1+t/t0): logarithmic creep aging [PE]
    
    References: Packaging creep models for MEMS (general viscoelastic literature).
    Exact parameters are device/foundry-specific [UA].
    All magnitudes are [SA] synthetic baselines.
    """
    def __init__(
        self,
        base_zro_dps: float = 0.05,
        relaxation_amplitude_dps: float = 0.03,
        relaxation_tau_hours: float = 20.0,
        creep_rate_dps: float = 0.008,
        creep_t0_hours: float = 5.0,
    ):
        self.base_zro = base_zro_dps
        self.A = relaxation_amplitude_dps
        self.tau = relaxation_tau_hours
        self.B = creep_rate_dps
        self.t0 = creep_t0_hours

    def generate_trajectory(self, num_hours: int = 168, profile: str = "NOMINAL") -> list:
        trajectory = []
        for hour in range(num_hours + 1):
            # Viscoelastic relaxation component [PE]
            relaxation = self.A * (1.0 - np.exp(-hour / self.tau))
            # Logarithmic creep aging [PE]
            creep = self.B * np.log(1.0 + hour / self.t0)

            zro = self.base_zro + relaxation + creep

            if profile == "NOMINAL":
                pass  # baseline
            elif profile == "MEMS_STICTION_ONSET":
                # ZRO anomaly: sudden large step if stiction threshold approached
                if hour >= 48:
                    zro += 0.12 * (1.0 + (hour - 48) / 120.0)
            elif profile == "PACKAGING_STRESS_RELAXATION":
                # Accelerated relaxation from aggressive die attach stress
                zro = self.base_zro + 2.5 * self.A * (1.0 - np.exp(-hour / (self.tau * 0.4)))
            elif profile == "SPATIAL_OUTLIER":
                # High baseline ZRO outlier on lot edge [SA]
                zro = 0.38 + relaxation * 0.5 + creep * 0.5
            elif profile == "THERMAL_RUNAWAY":
                # Capacitive comb geometry deformation under high thermal load
                if hour >= 24:
                    zro += 0.002 * (hour - 24)

            noise = np.random.normal(0, 0.002)
            zro = max(0.0, zro + noise)
            trajectory.append(round(float(zro), 5))
        return trajectory


# ===========================================================================
# IMAGE SENSOR — Shockley-Read-Hall Dark Current Model
# ===========================================================================
class SRHDarkCurrentModel:
    """
    [PE] CMOS Image Sensor dark current model based on Shockley-Read-Hall (SRH)
    thermal generation in depletion region.

    I_dark(T) ∝ ni(T) ∝ exp(-Eg / 2kT)

    Dark current grows with time as trap density increases (burn-in accelerates trap buildup).
    Hot pixels are localized high-generation sites (crystal defects) [PE].

    Reference: Shockley-Read-Hall recombination theory (general semiconductor physics).
    Exact magnitudes are device/foundry-specific [UA]; all values here are [SA].
    """
    def __init__(
        self,
        base_dark_current_nA_cm2: float = 1.5,
        stress_temp_c: float = 60.0,
        activation_energy_eV: float = 0.55,
    ):
        self.base_dc = base_dark_current_nA_cm2
        self.T_stress_K = stress_temp_c + 273.15
        self.Ea = activation_energy_eV
        self.k_b = 8.617333262145e-5  # eV/K [PE]

    def _thermal_factor(self, temp_k: float) -> float:
        """SRH thermal scaling factor relative to reference [PE]."""
        T_ref_K = 300.0  # 27°C reference
        return np.exp(-self.Ea / (self.k_b * temp_k)) / np.exp(-self.Ea / (self.k_b * T_ref_K))

    def generate_trajectory(self, num_hours: int = 168, profile: str = "NOMINAL") -> list:
        trajectory = []
        thermal_factor = self._thermal_factor(self.T_stress_K)

        for hour in range(num_hours + 1):
            # Trap density grows with time under thermal stress [PE]
            trap_growth = 1.0 + 0.0015 * hour

            dc = self.base_dc * thermal_factor * trap_growth

            if profile == "NOMINAL":
                pass
            elif profile == "DARK_CURRENT_SPIKE_GROWTH":
                # Localized defect cluster activation [PE]
                if hour >= 48:
                    dc *= 1.0 + 0.025 * (hour - 48)
            elif profile == "THERMAL_RUNAWAY":
                # Global trap generation acceleration
                if hour >= 24:
                    dc *= np.exp(0.012 * (hour - 24))
            elif profile == "SPATIAL_OUTLIER":
                # High dark-current outlier pixel cluster [SA]
                dc = self.base_dc * thermal_factor * trap_growth * 4.0
            elif profile == "DIELECTRIC_OSCILLATION":
                # Cycling dark current from periodic thermal shock [SA]
                osc = 0.8 * np.sin(2 * np.pi * hour / 24.0)
                dc = max(0.1, dc + osc)

            noise = np.random.normal(0, 0.03)
            dc = max(0.05, dc + noise)
            trajectory.append(round(float(dc), 4))
        return trajectory
