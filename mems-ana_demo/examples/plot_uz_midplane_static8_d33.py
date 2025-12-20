# examples/plot_uz_midplane_static8_d33.py
# -*- coding: utf-8 -*-
"""
8 panels (2×4) uz(x,y) 3D surfaces

Row/branch:
- Top row   : rising  (P_up branch)
- Bottom row: falling (P_down branch)

Column order (match butterfly reading):
- Vc (where P=0 on that branch) -> 0 V -> ±15 V -> ±30 V

Model (schematic, consistent with butterfly):
- Vbot = 0 (GND), ΔV = Vtop - Vbot = Vtop      [V]
- Ez = ΔV / t_pzt                              [V/m]
- P(Ez) from hysteresis branches (make_closed_loop)
- Strain (schematic):
    S3(E) = d33*(P/Pm)*Ez + Q*P^2
- Displacement amplitude (unit-shape max):
    uz0(V) = S3(V) * t_pzt
- Surface:
    uz(x,y) = uz0(V) * shape(x,y)

Geometry / support intent:
- x edges supported (CAV wall) -> uz=0 at x=0, Lx
- y edges free (flow channel)  -> not forced to 0 at y=0, Wy

Display:
- Positive-only (clip uz < 0 to 0)
- Color fixed: 0..500 nm
- z-axis TRUE range: 0..500 nm (labels)
- z VISUALLY stretched by plotting Z*Z_EXAG (tick labels remain nm)
- x,y aspect kept (200 µm vs 500 µm)

V–I note:
- This script uses V only; current I is not modeled.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize

# ---- import safety: editable install無しでも動く ----
try:
    from mems_ana.ferroelectric import make_closed_loop
except ModuleNotFoundError:
    import sys
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))
    from mems_ana.ferroelectric import make_closed_loop


# =========================
# Geometry
# =========================
Lx = 200e-6      # [m]
Wy = 500e-6      # [m]
t_pzt = 1.2e-6   # [m]

nx, ny = 120, 160

# =========================
# Drive (V–I 系の V 側のみ; Iは未モデル)
# =========================
Vmax = 30.0
Vmid = 15.0

# =========================
# Ferroelectric loop params
# =========================
Pm_uC_cm2 = 42.0
Pr_target_uC_cm2 = 30.0
Ec_V_per_m = 5e6

# =========================
# d33 / electrostriction knobs
# =========================
d33 = 250e-12      # [m/V]
Q = 0.03           # [m^4/C^2]

# =========================
# Display knobs
# =========================
POSITIVE_ONLY = True

UZ_MAX_NM = 500.0        # color range 0..500 nm
TARGET_PEAK_NM = 500.0   # calibrate: (+30 V, rising) peak -> 500 nm

Z_EXAG = 60.0            # 描画Zのみ誇張（tickはnmに戻す）
VIEW_ELEV = 28
VIEW_AZIM = -60

# タイトル重なり回避
FIGSIZE = (22, 9)
SUBPLOTS_ADJUST = dict(left=0.03, right=0.86, bottom=0.06, top=0.82, wspace=0.06, hspace=0.22)
SUPTITLE_Y = 0.97


def shape_xy(X: np.ndarray, Y: np.ndarray, Lx_: float, Wy_: float) -> np.ndarray:
    """
    intent:
    - x edges supported -> uz=0 at x=0, Lx
    - y edges free      -> not forced to 0 at y=0, Wy
    """
    # x: clamped-like (0 at edges)
    sx = np.sin(np.pi * X / Lx_) ** 2

    # y: free-like (not 0 at edges)
    a = 0.20
    sy = 1.0 - a * (1.0 + np.cos(2.0 * np.pi * Y / Wy_)) / 2.0
    return sx * sy


def build_loop() -> dict[str, np.ndarray]:
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
    loop["Ez_sweep_V_per_m"] = Ez_sweep

    print(f"Ec = {Ec_V_per_m/1e6:.2f} MV/m, Es = {loop['Es_V_per_m']/1e6:.2f} MV/m")
    print(f"Pr (rising)  @E≈0 = {loop['Pr_rising_uC_cm2']:.2f} µC/cm²")
    print(f"Pr (falling) @E≈0 = {loop['Pr_falling_uC_cm2']:.2f} µC/cm²")
    return loop


def interp_P_uC_cm2(Ez: float, loop: dict[str, np.ndarray], branch: str) -> float:
    Ez_grid = loop["Ez_sweep_V_per_m"]
    if branch == "up":
        P = loop["P_up_uC_cm2"]
    elif branch == "down":
        P = loop["P_down_uC_cm2"]
    else:
        raise ValueError("branch must be 'up' or 'down'")
    return float(np.interp(Ez, Ez_grid, P))


def find_Vc_for_branch(loop: dict[str, np.ndarray], branch: str) -> float:
    """
    Find Vc for each branch where P(E)=0 (linear interpolation).
    Returns Vtop [V] such that P≈0 on that branch.
    """
    Ez_grid = loop["Ez_sweep_V_per_m"]
    if branch == "up":
        P = loop["P_up_uC_cm2"]
    elif branch == "down":
        P = loop["P_down_uC_cm2"]
    else:
        raise ValueError("branch must be 'up' or 'down'")

    # find sign change (or exact zero)
    s = np.sign(P)
    idx = np.where(s[:-1] * s[1:] <= 0)[0]
    if len(idx) == 0:
        # fallback: choose minimum |P|
        i = int(np.argmin(np.abs(P)))
        Ez0 = float(Ez_grid[i])
        return float(Ez0 * t_pzt)

    i = int(idx[0])
    E1, E2 = float(Ez_grid[i]), float(Ez_grid[i + 1])
    P1, P2 = float(P[i]), float(P[i + 1])

    # linear interpolation to P=0
    Ez0 = E1 + (0.0 - P1) * (E2 - E1) / (P2 - P1 + 1e-30)
    return float(Ez0 * t_pzt)


def uz_abs_nm_from_V(V: float, loop: dict[str, np.ndarray], branch: str) -> float:
    """
    Absolute uz amplitude [nm] at unit-shape max (before shape(x,y)).
    Consistent with butterfly: S3 = d33*(P/Pm)*E + Q*P^2
    """
    Ez = V / t_pzt
    P_uC_cm2 = interp_P_uC_cm2(Ez, loop, branch)

    # 1 µC/cm² = 0.01 C/m²
    P = P_uC_cm2 * 0.01
    Pm = Pm_uC_cm2 * 0.01

    d33_eff = d33 * (P / Pm)   # P=0 -> d33_eff=0
    S_lin = d33_eff * Ez
    S_q = Q * (P ** 2)         # P=0 -> 0

    uz_m = (S_lin + S_q) * t_pzt
    return float(uz_m * 1e9)   # [nm]


def main() -> None:
    outdir = Path("outputs") / "figs"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "uz_midplane_static8_d33_matchButterflyAbs_fixed0to500nm_ZEXAG.png"

    # grid
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Wy, ny)
    X, Y = np.meshgrid(x, y, indexing="xy")
    X_um = X * 1e6
    Y_um = Y * 1e6
    Lx_um = Lx * 1e6
    Wy_um = Wy * 1e6

    # loop + Vc
    loop = build_loop()
    Vc_up = find_Vc_for_branch(loop, "up")
    Vc_dn = find_Vc_for_branch(loop, "down")

    # column order: Vc -> 0 -> 15 -> 30
    voltages_top = [Vc_up, 0.0, +Vmid, +Vmax]
    voltages_bot = [Vc_dn, 0.0, -Vmid, -Vmax]

    # shape
    S = shape_xy(X, Y, Lx, Wy)
    Smax = float(np.max(S))

    # ---- mechanical gain calibration (match butterfly scaling)
    # peak on surface at (+30V, rising) should be TARGET_PEAK_NM (at shape max)
    raw_u0_peak_nm = uz_abs_nm_from_V(+Vmax, loop, branch="up")
    raw_peak_surface_nm = raw_u0_peak_nm * Smax

    if raw_peak_surface_nm <= 0:
        G = 1.0
        print("WARN: raw peak <= 0, gain=1.0")
    else:
        G = TARGET_PEAK_NM / raw_peak_surface_nm

    print(f"Vc(up)   = {Vc_up:+.3f} V  (P_up=0)")
    print(f"Vc(down) = {Vc_dn:+.3f} V  (P_down=0)")
    print(f"Raw peak surface (+{Vmax:.0f} V, rising) = {raw_peak_surface_nm:.3f} nm (before gain)")
    print(f"Mechanical gain G = {G:.3f} -> target peak {TARGET_PEAK_NM:.1f} nm")

    # ---- compute all surfaces in nm
    def surface_nm(branch: str, V: float) -> np.ndarray:
        u0_nm = uz_abs_nm_from_V(V, loop, branch=branch) * G
        U_nm = u0_nm * S
        if POSITIVE_ONLY:
            U_nm = np.clip(U_nm, 0.0, None)
        return U_nm

    U_top = [surface_nm("up", V) for V in voltages_top]
    U_bot = [surface_nm("down", V) for V in voltages_bot]

    # ---- color scale 0..500 nm
    cmap = mpl.colormaps["viridis"]
    norm = Normalize(vmin=0.0, vmax=UZ_MAX_NM)

    # ---- plot
    fig, axs = plt.subplots(2, 4, figsize=FIGSIZE, subplot_kw={"projection": "3d"})
    fig.subplots_adjust(**SUBPLOTS_ADJUST)

    def title_for(branch: str, V: float, is_vc: bool) -> str:
        if is_vc:
            tag = "Vc(up)" if branch == "up" else "Vc(down)"
            return f"uz(x,y) @ Vtop={V:+.2f} V ({tag})"
        else:
            br = "rising" if branch == "up" else "falling"
            return f"uz(x,y) @ Vtop={V:+.2f} V ({br})"

    def plot_one(ax, U_nm: np.ndarray, title: str):
        # plot Z only exaggerated
        Z_plot_um = (U_nm / 1000.0) * Z_EXAG  # nm -> µm -> *Z_EXAG
        facecolors = cmap(norm(U_nm))

        ax.plot_surface(
            X_um, Y_um, Z_plot_um,
            facecolors=facecolors,
            linewidth=0,
            antialiased=True,
            shade=False,
        )

        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x [µm]")
        ax.set_ylabel("y [µm]")
        ax.set_xlim(0, Lx_um)
        ax.set_ylim(0, Wy_um)

        # z true range 0..500 nm -> plotted range with Z_EXAG
        zmax_plot_um = (UZ_MAX_NM / 1000.0) * Z_EXAG
        ax.set_zlim(0.0, zmax_plot_um)

        # z ticks labeled in nm
        tick_nm = [0, 250, 500]
        tick_um_plot = [(t / 1000.0) * Z_EXAG for t in tick_nm]
        ax.set_zticks(tick_um_plot)
        ax.set_zticklabels([str(t) for t in tick_nm])
        ax.set_zlabel("uz [nm]")

        # keep x:y physical aspect (200 vs 500)
        try:
            ax.set_box_aspect((1.0, Wy_um / Lx_um, 0.35))
        except Exception:
            pass

        ax.view_init(elev=VIEW_ELEV, azim=VIEW_AZIM)

    # top row
    for j, V in enumerate(voltages_top):
        is_vc = (j == 0)
        plot_one(axs[0, j], U_top[j], title_for("up", V, is_vc=is_vc))

    # bottom row
    for j, V in enumerate(voltages_bot):
        is_vc = (j == 0)
        plot_one(axs[1, j], U_bot[j], title_for("down", V, is_vc=is_vc))

    fig.suptitle(
        "d33-dominated uz(x,y) (positive-only) | ABSOLUTE uz(V) consistent with butterfly\n"
        "S = d33*(P/Pm)*E + Q*P^2  |  Color fixed: 0–500 nm  |  z(true): 0–500 nm  |  "
        f"Z_EXAG={Z_EXAG:.0f}\n"
        "x-edges supported / y-edges free (schematic)  |  V–I: current I not modeled  |  "
        f"Vc(up)={Vc_up:+.2f} V, Vc(down)={Vc_dn:+.2f} V",
        fontsize=13,
        y=SUPTITLE_Y,
    )

    # colorbar (nm)
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cax = fig.add_axes([0.88, 0.14, 0.015, 0.68])
    cb = fig.colorbar(sm, cax=cax)
    cb.set_label("uz [nm] (color range)")

    plt.savefig(outpath, dpi=180)
    plt.show()
    print(f"Saved: {outpath.resolve()}")

    # quick sanity prints (surface max at shape max)
    def peak_nm(U_nm: np.ndarray) -> float:
        return float(np.max(U_nm))

    print("Sanity peaks (after scaling, at shape max, positive-only):")
    print(f"  rising  Vc   -> {peak_nm(U_top[0]):.2f} nm (should be ~0)")
    print(f"  rising  0V   -> {peak_nm(U_top[1]):.2f} nm (offset allowed)")
    print(f"  rising  15V  -> {peak_nm(U_top[2]):.2f} nm")
    print(f"  rising  30V  -> {peak_nm(U_top[3]):.2f} nm (should be ~{TARGET_PEAK_NM:.0f})")
    print(f"  falling Vc   -> {peak_nm(U_bot[0]):.2f} nm (should be ~0)")
    print(f"  falling 0V   -> {peak_nm(U_bot[1]):.2f} nm (offset allowed)")
    print(f"  falling -15V -> {peak_nm(U_bot[2]):.2f} nm")
    print(f"  falling -30V -> {peak_nm(U_bot[3]):.2f} nm (should be ~{TARGET_PEAK_NM:.0f})")


if __name__ == "__main__":
    main()
