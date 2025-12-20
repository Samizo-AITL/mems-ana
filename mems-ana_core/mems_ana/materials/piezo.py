from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Piezo:
    E: float
    nu: float
    rho: float
    eps_r: float
    d31: float
    tan_delta: float


# ===== alias（全事故防止） =====
PiezoMaterial = Piezo
PiezoMat = Piezo
