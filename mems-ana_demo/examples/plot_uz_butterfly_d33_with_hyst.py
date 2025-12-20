# examples/plot_uz_butterfly_d33_with_hyst.py
# -*- coding: utf-8 -*-
"""
u–V Butterfly (schematic)

- Vbot = GND, ΔV = Vtop - Vbot = Vtop  [V]
- Ez = ΔV / t_pzt                      [V/m]
- P(Ez) hysteresis (simple)
- Strain:
    S3 = d33_0 * (P/Pm) * Ez  +  Q * P^2
- uz ≈ S3 * t_pzt

This version:
- Keeps the original butterfly behavior.
- ONLY adds mechanical gain calibration so that the reference peak becomes 500 nm.
- Fixes y-axis to 0..500 nm (and optionally clips).
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ---- import safety: editable install無しでも動く ----
try:
    from mems_ana.ferroelectric import make_closed_loop
except ModuleNotFoundError:
    import sys
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))
    from mems_ana.ferroelectric import make_closed_loop


def main() -> None:
    OUTDIR = Path("outputs") / "figs"
    OUTDIR.mkdir(parents=True, exist_ok=True)
    outpath = OUTDIR / "uz_butterfly_d33_hyst_scaled_0to500nm.png"

    # ============================
    # 注記用（このスクリプトは1点評価）
    # ============================
    x_eval_um = 50.0
    y_eval_um = 250.0

    # ============================
    # Drive (V–I の V 側。I は未モデル)
    # ============================
    Vmax = 30.0
    t_pzt = 1.2e-6

    # 滑らかパス（-Vmax→+Vmax→-Vmax）
    n_half = 2000
    V_up = np.linspace(-Vmax, +Vmax, n_half)  # rising
    V_dn = np.linspace(+Vmax, -Vmax, n_half)  # falling
    V_path = np.concatenate([V_up, V_dn[1:]])  # 重複点除去

    Ez_path = V_path / t_pzt
    n_up = len(V_up)

    # ============================
    # P(Ez) hysteresis parameters
    # ============================
    Pm_uC_cm2 = 42.0
    Pr_target_uC_cm2 = 30.0
    Ec_V_per_m = 5e6  # ここは元のまま

    Ez_max = Vmax / t_pzt
    Ez_sweep = np.linspace(-Ez_max, +Ez_max, 5000)

    loop = make_closed_loop(
        Ez_sweep,
        Ec_V_per_m=Ec_V_per_m,
        Pm_uC_cm2=Pm_uC_cm2,
        Pr_target_uC_cm2=Pr_target_uC_cm2,
        Es_V_per_m=None,
        n_jump=200,
    )

    P_up_uC_cm2 = loop["P_up_uC_cm2"]
    P_dn_uC_cm2 = loop["P_down_uC_cm2"]

    def interp_P(branch: np.ndarray, Ez_query: np.ndarray) -> np.ndarray:
        return np.interp(Ez_query, Ez_sweep, branch)

    # 上り/下りで枝を切替
    P_up_path = interp_P(P_up_uC_cm2, Ez_path[:n_up])
    P_dn_path = interp_P(P_dn_uC_cm2, Ez_path[n_up - 1 :])
    P_path_uC_cm2 = np.concatenate([P_up_path, P_dn_path[1:]])

    # 単位変換：1 µC/cm² = 0.01 C/m²
    P_path_C_m2 = P_path_uC_cm2 * 0.01
    Pm_C_m2 = Pm_uC_cm2 * 0.01

    # ============================
    # uz model (schematic)  ※元の形を維持
    # ============================
    d33_0 = 250e-12  # [m/V]
    Q = 0.03         # [m^4/C^2]

    pol = np.clip(P_path_C_m2 / Pm_C_m2, -1.0, 1.0)
    S_lin = d33_0 * pol * Ez_path
    S_q = Q * (P_path_C_m2 ** 2)

    uz_m = (S_lin + S_q) * t_pzt
    uz_nm = uz_m * 1e9  # [nm]

    # ============================
    # ここが今回の「簡単な要求」：縦軸を 0..500 nm に合わせる
    # ============================
    TARGET_PEAK_NM = 500.0
    FIX_YLIM = True
    CLIP_TO_RANGE = True

    # 参照ピーク：rising の +Vmax の点（※あなたの3D校正と同じ基準にしやすい）
    idx_ref = n_up - 1  # rising の +Vmax
    peak_ref_nm = float(uz_nm[idx_ref])

    if peak_ref_nm == 0.0:
        G_mech = 1.0
        print("WARN: peak_ref_nm is zero. G_mech forced to 1.0")
    else:
        G_mech = TARGET_PEAK_NM / peak_ref_nm

    uz_nm = uz_nm * G_mech

    if CLIP_TO_RANGE:
        uz_nm = np.clip(uz_nm, 0.0, TARGET_PEAK_NM)

    # ============================
    # Plot
    # ============================
    plt.figure(figsize=(8, 5))
    plt.plot(V_path, uz_nm, lw=2)
    plt.axhline(0, lw=1)
    plt.axvline(0, lw=1)
    plt.grid(True)

    if FIX_YLIM:
        plt.ylim(0, TARGET_PEAK_NM)

    plt.xlabel("Top electrode voltage Vtop [V] (Vbot=GND, ΔV=Vtop)  |  I not modeled")
    plt.ylabel("uz [nm] (schematic, scaled)")
    plt.title(
        "u–V Butterfly (schematic)\n"
        "S = d33·(P/Pm)·Ez + Q·P(Ez)^2  (P from P–Ez hysteresis branches)\n"
        f"Scaled so that uz(+{Vmax:.0f} V, rising) = {TARGET_PEAK_NM:.0f} nm\n"
        f"x={x_eval_um:.0f} µm, y={y_eval_um:.0f} µm, Vtop=±{Vmax:.0f} V"
    )
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.show()

    print(f"Saved: {outpath.resolve()}")
    print(f"Ec = {Ec_V_per_m/1e6:.2f} MV/m, Es = {loop['Es_V_per_m']/1e6:.2f} MV/m")
    print(f"Pr (rising)  @E≈0 = {loop['Pr_rising_uC_cm2']:.2f} µC/cm²")
    print(f"Pr (falling) @E≈0 = {loop['Pr_falling_uC_cm2']:.2f} µC/cm²")
    print(f"Raw peak ref (rising @ +{Vmax:.0f} V) = {peak_ref_nm:.3f} nm")
    print(f"Mechanical gain G_mech = {G_mech:.3f} -> target peak = {TARGET_PEAK_NM:.1f} nm")


if __name__ == "__main__":
    main()
