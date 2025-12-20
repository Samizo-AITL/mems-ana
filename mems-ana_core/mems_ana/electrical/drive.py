from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SinDrive:
    V_rms: float  # [V]
    f_hz: float   # [Hz]
