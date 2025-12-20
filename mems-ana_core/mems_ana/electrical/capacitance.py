from __future__ import annotations
import numpy as np

EPS0 = 8.8541878128e-12

def capacitance_parallel_plate(eps_r: float, area: float, t_pzt: float, area_ratio: float = 1.0) -> float:
    if t_pzt <= 0.0:
        return 0.0
    return EPS0 * eps_r * (area * area_ratio) / t_pzt

def admittance_dielectric(C: float, omega: float, tan_delta: float) -> complex:
    # Y = jωC + ωC*tanδ
    return 1j * omega * C + (omega * C * tan_delta)
