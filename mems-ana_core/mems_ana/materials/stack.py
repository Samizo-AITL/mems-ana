from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from mems_ana.materials.elastic import IsoElastic
from mems_ana.materials.piezo import PiezoMat


@dataclass(frozen=True)
class Stack:
    """
    Unimorph laminate stack (base + piezo)

    z = 0 at bottom of base layer
    """
    base: IsoElastic
    t_base: float            # [m]
    piezo: Optional[PiezoMat] = None
    t_pzt: float = 0.0       # [m]
    elec_area_ratio: float = 1.0

    # ---------- helpers ----------
    def _Q(self, E: float, nu: float) -> float:
        return E / (1.0 - nu**2)

    def t_total(self) -> float:
        return self.t_base + (self.t_pzt if self.piezo else 0.0)

    def areal_mass(self) -> float:
        m = self.base.rho * self.t_base
        if self.piezo and self.piezo.rho > 0.0:
            m += self.piezo.rho * self.t_pzt
        return m

    # ---------- neutral axis ----------
    def neutral_axis_z0(self) -> float:
        Qb = self._Q(self.base.E, self.base.nu)
        zb = 0.5 * self.t_base

        num = Qb * self.t_base * zb
        den = Qb * self.t_base

        if self.piezo and self.t_pzt > 0.0:
            Qp = Qb  # minimal (can extend later)
            zp = self.t_base + 0.5 * self.t_pzt
            num += Qp * self.t_pzt * zp
            den += Qp * self.t_pzt

        return num / den

    # ---------- bending stiffness ----------
    def D_plate(self) -> float:
        z0 = self.neutral_axis_z0()
        Qb = self._Q(self.base.E, self.base.nu)
        zb = 0.5 * self.t_base

        D = Qb * ((self.t_base**3) / 12.0 + self.t_base * (zb - z0) ** 2)

        if self.piezo and self.t_pzt > 0.0:
            Qp = Qb
            zp = self.t_base + 0.5 * self.t_pzt
            D += Qp * ((self.t_pzt**3) / 12.0 + self.t_pzt * (zp - z0) ** 2)

        return D

    # ---------- piezo actuation ----------
    def piezo_eigenstrain(self, V_peak: float) -> float:
        if self.piezo is None or self.t_pzt <= 0.0:
            return 0.0
        return self.piezo.d31 * (V_peak / self.t_pzt)

    def piezo_bending_moment_per_width(self, V_peak: float) -> float:
        if self.piezo is None or self.t_pzt <= 0.0:
            return 0.0

        z0 = self.neutral_axis_z0()
        eps0 = self.piezo_eigenstrain(V_peak)

        Qp = self._Q(self.base.E, self.base.nu)
        zp = self.t_base + 0.5 * self.t_pzt

        M0 = Qp * eps0 * self.t_pzt * (zp - z0)
        M0 *= self.elec_area_ratio

        return M0
