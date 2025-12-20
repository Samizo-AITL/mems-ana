from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RectPlate:
    """Rectangular diaphragm (a x b), thickness is handled by stack/material."""
    a: float  # [m] length in x
    b: float  # [m] length in y

    def area(self) -> float:
        return self.a * self.b
