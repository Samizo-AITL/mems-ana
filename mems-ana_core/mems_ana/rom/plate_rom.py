from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from mems_ana.geometry.plate import RectPlate
from mems_ana.materials.stack import Stack
from mems_ana.physics.plate_theory import omega_mn_simply_supported, clamp_correction_factor
from mems_ana.electrical.capacitance import capacitance_parallel_plate
from mems_ana.electrical.terminal import terminal_current_rms


@dataclass(frozen=True)
class Mode:
    m: int
    n: int


class RectPlateROM:
    """
    Rectangular plate ROM (plate + piezo unimorph)
    - Mechanical: modal FRF for center uz
    - Electrical: terminal V–I (capacitive + dielectric loss)
    - K_W: 1-point calibrated shape factor converting curvature scale to center displacement scale

    Notes:
    - This ROM uses a simplified modal normalization (unit modal mass assumption).
    - K_W is a pragmatic calibration knob to absorb mode-shape / BC / normalization mismatches.
    """

    def __init__(
        self,
        plate: RectPlate,
        stack: Stack,
        modes: list[Mode] | None = None,
        K_W: float = 8.0,  # shape factor (calibrate once)
    ) -> None:
        self.plate = plate
        self.stack = stack
        self.modes = modes if modes else [Mode(1, 1), Mode(2, 1), Mode(1, 2), Mode(2, 2)]
        self.K_W = float(K_W)

        if self.K_W <= 0.0:
            raise ValueError("K_W must be positive.")

    # ---------- eigen ----------
    def modal_freqs_hz(self) -> dict[tuple[int, int], float]:
        D = self.stack.D_plate()
        m_areal = self.stack.areal_mass()
        k = clamp_correction_factor()

        out: dict[tuple[int, int], float] = {}
        for md in self.modes:
            w = k * omega_mn_simply_supported(D, m_areal, self.plate.a, self.plate.b, md.m, md.n)
            out[(md.m, md.n)] = w / (2.0 * np.pi)
        return out

    # ---------- electrical ----------
    def capacitance(self) -> float:
        if self.stack.piezo is None or self.stack.t_pzt <= 0.0:
            return 0.0

        return capacitance_parallel_plate(
            eps_r=self.stack.piezo.eps_r,
            area=self.plate.area(),
            t_pzt=self.stack.t_pzt,
            area_ratio=self.stack.elec_area_ratio,
        )

    # ---------- FRF ----------
    def frf_center_uz_and_I(self, V_rms: float, f_hz: float, zeta: float = 0.02) -> tuple[float, float]:
        """
        Return:
          - |uz_center| [m] (magnitude)
          - I_rms [A]

        Inputs:
          - V_rms [V]
          - f_hz  [Hz]
          - zeta  [-] modal damping ratio (uniform)
        """
        omega = 2.0 * np.pi * f_hz

        # ---- electrical (terminal V–I) ----
        C = self.capacitance()
        tan_delta = self.stack.piezo.tan_delta if self.stack.piezo else 0.0
        I_rms = terminal_current_rms(V_rms, omega, C, tan_delta)

        # ---- mechanical (center uz) ----
        if self.stack.piezo is None or self.stack.t_pzt <= 0.0:
            return 0.0, float(I_rms)

        V_peak = V_rms * np.sqrt(2.0)

        D = self.stack.D_plate()
        if D <= 0.0:
            return 0.0, float(I_rms)

        # Piezo-induced bending moment per width -> curvature
        M0 = self.stack.piezo_bending_moment_per_width(V_peak)  # [N]
        kappa = M0 / D  # [1/m]

        # Curvature -> center displacement scale
        # IMPORTANT:
        #   If K_W is a "shape factor" that you calibrate to match FEM/measurement,
        #   center deflection should scale proportionally with K_W.
        #   (If you keep division here, increasing K_W would shrink uz, which is counter-intuitive.)
        w_scale = self.K_W * kappa * (self.plate.a ** 2)  # [m] scale

        uz = 0.0 + 0.0j
        m_areal = self.stack.areal_mass()
        k_clamp = clamp_correction_factor()

        # Modal superposition at center (x=a/2, y=b/2)
        for md in self.modes:
            w_mn = k_clamp * omega_mn_simply_supported(
                D, m_areal, self.plate.a, self.plate.b, md.m, md.n
            )

            # simply-supported mode shape at center:
            # phi(x,y) = sin(mπx/a) sin(nπy/b), at center -> sin(mπ/2) sin(nπ/2)
            phi_c = np.sin(md.m * np.pi * 0.5) * np.sin(md.n * np.pi * 0.5)
            if abs(phi_c) < 1e-12:
                continue

            # SDOF FRF (unit-normalized) with damping
            H = 1.0 / ((w_mn**2 - omega**2) + 1j * (2.0 * zeta * w_mn * omega))

            uz += (w_scale * phi_c) * H

        return float(abs(uz)), float(I_rms)
