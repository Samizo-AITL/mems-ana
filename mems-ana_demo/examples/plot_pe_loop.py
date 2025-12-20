# -*- coding: utf-8 -*-
"""
plot_pe_loop.py

Purpose:
- P–Ez ヒステリシス（閉ループ）を描いて、形と Pr を確認します。
- ΔV = Vtop - Vbot, Vbot = GND
- Ez = ΔV / t_pzt の流儀を維持します。

Note:
- ここでは I（電流）は扱わず、V（電圧）→ E（電界）→ P（分極）を可視化します。
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from mems_ana.ferroelectric import make_closed_loop


def main() -> None:
    outdir = Path("outputs/figs")
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "pzt_pe_hysteresis_1d.png"

    # ===== parameters (edit here) =====
    Pm = 42.0         # [µC/cm^2]
    Pr_target = 30.0  # [µC/cm^2]
    Vmax = 30.0       # [V]  (Vtop max, Vbot=GND)
    t_pzt = 1.2e-6    # [m]
    Ec = 5e6          # [V/m] width scale

    # Ez sweep: -Ezmax -> +Ezmax
    Ez_max = Vmax / t_pzt
    Ez = np.linspace(-Ez_max, +Ez_max, 2000)

    loop = make_closed_loop(
        Ez,
        Ec_V_per_m=Ec,
        Pm_uC_cm2=Pm,
        Pr_target_uC_cm2=Pr_target,
        Es_V_per_m=None,
        n_jump=120,
    )

    Eloop = loop["Eloop_V_per_m"]
    Ploop = loop["Ploop_uC_cm2"]

    print(f"Pm = {Pm:.2f} µC/cm², Pr_target = {Pr_target:.2f} µC/cm²")
    print(f"Ec = {Ec/1e6:.2f} MV/m, Es = {loop['Es_V_per_m']/1e6:.2f} MV/m")
    print(f"Pr (rising)  @E≈0 = {loop['Pr_rising_uC_cm2']:.2f} µC/cm²")
    print(f"Pr (falling) @E≈0 = {loop['Pr_falling_uC_cm2']:.2f} µC/cm²")

    plt.figure(figsize=(7, 5))
    plt.plot(Eloop / 1e6, Ploop, lw=2)
    plt.xlabel("Ez [MV/m]")
    plt.ylabel("P [µC/cm²]")
    plt.title(f"Closed P–Ez Loop (Vtop=±{Vmax:.0f} V, Vbot=GND)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.show()

    print(f"Saved: {outpath.resolve()}")


if __name__ == "__main__":
    main()
