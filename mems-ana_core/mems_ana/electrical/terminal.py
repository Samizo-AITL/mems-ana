from __future__ import annotations
import numpy as np
from mems_ana.electrical.capacitance import admittance_dielectric

def terminal_current_rms(V_rms: float, omega: float, C: float, tan_delta: float) -> float:
    Y = admittance_dielectric(C, omega, tan_delta)
    return float(abs(Y) * V_rms)
