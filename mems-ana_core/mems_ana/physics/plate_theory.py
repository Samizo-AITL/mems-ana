from __future__ import annotations
import numpy as np

def omega_mn_simply_supported(D: float, m_areal: float, a: float, b: float, m: int, n: int) -> float:
    """
    Simply-supported rectangular plate:
      ω_mn^2 = (D/m_areal) * ( (mπ/a)^2 + (nπ/b)^2 )^2
    """
    kx = m * np.pi / a
    ky = n * np.pi / b
    return np.sqrt((D / m_areal) * (kx**2 + ky**2) ** 2)

def clamp_correction_factor() -> float:
    """
    Crude correction to approximate clamped boundary frequencies from simply-supported.
    Keep constant for now to avoid parameter explosion.
    """
    return 1.25
