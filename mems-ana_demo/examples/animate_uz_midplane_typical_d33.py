# examples/animate_uz_midplane_typical_d33.py
# -*- coding: utf-8 -*-
"""
animate_uz_midplane_typical_d33.py

Purpose:
- 8枚プロット（plot_uz_midplane_static8_d33.py）の「ABSOLUTE uz(V) consistent with butterfly」仕様に合わせて
  uz(x,y) 3D 表示を GIF 化する。
- モデル式（8枚と統一）:
    S(E) = d33*(P/Pm)*E + Q*P(E)^2
    uz(V) ≈ S(E)*t_pzt
  ※ P(E) は make_closed_loop の up/down 枝を使用

Display (8枚と統一):
- 正のみ表示: U_nm = clip(U_nm, 0, +inf)
- color range 固定: 0..500 nm
- z(true) 0..500 nm（ラベルは nm）、ただし描画のみ Z_EXAG 倍して見やすくする
- x-edges supported / y-edges free の shape_xy を使用
- V–I: 電流 I はモデル化しない（Vのみ）

Drive (V側):
- 1サイクルを「上り→下り」で連続に掃引（10サイクル）
- Vc(up), Vc(down) は P=0 になる電圧（up/down枝別）をループから自動推定して使用
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize
from PIL import Image

# ---- import safety ----
try:
    from mems_ana.ferroelectric import make_closed_loop
except ModuleNotFoundError:  # pragma: no cover
    import sys
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))
    from mems_ana.ferroelectric import make_closed_loop


# =========================
# Geometry / grid (8枚と統一)
# =========================
Lx = 200e-6      # [m]
Wy = 500e-6      # [m]
t_pzt = 1.2e-6   # [m]
nx, ny = 120, 160

# =========================
# Voltages (V only; I not modeled)
# =========================
Vmax = 30.0
Vmid = 15.0

n_cycles = 10

# 連続スイープの滑らかさ（増やすほど滑らか・重くなる）
N_SEG = 14  # 1区間あたりの分割

# =========================
# Ferroelectric loop params
# =========================
Pm_uC_cm2 = 42.0
Pr_target_uC_cm2 = 30.0
Ec_V_per_m = 5e6

# =========================
# d33 / electrostriction knobs (8枚と統一)
# =========================
d33 = 250e-12      # [m/V]
Q = 0.03           # [m^4/C^2] ここは「Q*P^2」に入れる

# =========================
# Display knobs (8枚と統一)
# =========================
POSITIVE_ONLY = True

UZ_MAX_NM = 500.0        # color range 0..500 nm
TARGET_PEAK_NM = 500.0   # 校正：(+30V, rising) の shape-max を 500 nm に合わせる

Z_EXAG = 60.0
VIEW_ELEV = 28
VIEW_AZIM = -60


def shape_xy(X: np.ndarray, Y: np.ndarray, Lx_: float, Wy_: float) -> np.ndarray:
    """
    8枚と同一の「実体っぽい」形：
    - x端支持 => uz=0 at x=0,Lx（sin^2）
    - y端自由 => y=0,Wy を強制0にしない（弱いy変化だけ入れる）
    """
    sx = np.sin(np.pi * X / Lx_) ** 2
    a = 0.20
    sy = 1.0 - a * (1.0 + np.cos(2.0 * np.pi * Y / Wy_)) / 2.0
    return sx * sy


def build_loop() -> dict[str, np.ndarray]:
    Ez_max = Vmax / t_pzt
    Ez_sweep = np.linspace(-Ez_max, +Ez_max, 3000)

    loop = make_closed_loop(
        Ez_sweep,
        Ec_V_per_m=Ec_V_per_m,
        Pm_uC_cm2=Pm_uC_cm2,
        Pr_target_uC_cm2=Pr_target_uC_cm2,
        Es_V_per_m=None,
        n_jump=160,
    )
    loop["Ez_sweep_V_per_m"] = Ez_sweep

    print(f"Ec = {Ec_V_per_m/1e6:.2f} MV/m, Es = {loop['Es_V_per_m']/1e6:.2f} MV/m")
    print(f"Pr (rising)  @E≈0 = {loop['Pr_rising_uC_cm2']:.2f} µC/cm²")
    print(f"Pr (falling) @E≈0 = {loop['Pr_falling_uC_cm2']:.2f} µC/cm²")
    return loop


def interp_P_uC_cm2(Ez: float, loop: dict[str, np.ndarray], branch: str) -> float:
    Ez_grid = loop["Ez_sweep_V_per_m"]
    if branch == "up":
        return float(np.interp(Ez, Ez_grid, loop["P_up_uC_cm2"]))
    if branch == "down":
        return float(np.interp(Ez, Ez_grid, loop["P_down_uC_cm2"]))
    raise ValueError("branch must be 'up' or 'down'")


def find_Vc_from_P0(loop: dict[str, np.ndarray], branch: str) -> float:
    """
    P(E)=0 となる電圧 Vc を、枝ごとに推定する。
    （8枚の Vc(up), Vc(down) に合わせるため）
    """
    Ez = loop["Ez_sweep_V_per_m"]
    if branch == "up":
        P = loop["P_up_uC_cm2"]
    elif branch == "down":
        P = loop["P_down_uC_cm2"]
    else:
        raise ValueError("branch must be 'up' or 'down'")

    s = np.sign(P)
    idx = np.where(np.diff(s) != 0)[0]
    if len(idx) == 0:
        # 交差が取れない場合は 0V 扱い
        return 0.0

    i = int(idx[np.argmin(np.abs(Ez[idx]))])  # 0付近の交差を優先
    # 線形補間で P=0
    E0, E1 = Ez[i], Ez[i + 1]
    P0, P1 = P[i], P[i + 1]
    if abs(P1 - P0) < 1e-30:
        Ez0 = E0
    else:
        Ez0 = E0 + (0.0 - P0) * (E1 - E0) / (P1 - P0)

    Vc = Ez0 * t_pzt
    return float(Vc)


def uz_abs_nm_from_V(V: float, loop: dict[str, np.ndarray], branch: str) -> float:
    """
    ABSOLUTE uz(V)（8枚/バタフライと統一）
      S = d33*(P/Pm)*E + Q*P^2
      uz = S*t_pzt
    """
    Ez = V / t_pzt

    P_uC_cm2 = interp_P_uC_cm2(Ez, loop, branch)
    P = P_uC_cm2 * 0.01         # 1 µC/cm² = 0.01 C/m²
    Pm = Pm_uC_cm2 * 0.01

    d33_eff = d33 * (P / Pm)
    S_lin = d33_eff * Ez
    S_q = Q * (P * P)           # ★ここが重要：Q*P^2（Ez^2ではない）

    uz_m = (S_lin + S_q) * t_pzt
    return float(uz_m * 1e9)    # [nm]


def make_path_from_keys(keys: list[float], n_seg: int) -> np.ndarray:
    """
    key電圧列を区間分割して滑らかな掃引を作る（単調増減を壊さない）
    """
    out: list[np.ndarray] = []
    for a, b in zip(keys[:-1], keys[1:]):
        out.append(np.linspace(a, b, n_seg, endpoint=False))
    out.append(np.array([keys[-1]]))
    return np.concatenate(out)


def pick_branch_by_slope(V_prev: float, V_now: float, V_next: float | None) -> str:
    """
    フレームの枝判定（上り/下り）：
    - 次があれば (V_next - V_now) の符号
    - 次が無ければ (V_now - V_prev) の符号
    """
    if V_next is None:
        d = V_now - V_prev
    else:
        d = V_next - V_now
    return "up" if d >= 0 else "down"


def main() -> None:
    out_anims = Path("outputs") / "anims"
    out_anims.mkdir(parents=True, exist_ok=True)
    gif_path = out_anims / "uz_midplane_typical_d33_10cycles.gif"

    # grid
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Wy, ny)
    X, Y = np.meshgrid(x, y, indexing="xy")
    X_um = X * 1e6
    Y_um = Y * 1e6

    # FE loop
    loop = build_loop()

    # Vc 推定（P=0）
    Vc_up = find_Vc_from_P0(loop, branch="up")
    Vc_down = find_Vc_from_P0(loop, branch="down")
    print(f"Vc(up)   (P=0) = {Vc_up:+.2f} V")
    print(f"Vc(down) (P=0) = {Vc_down:+.2f} V")

    # shape (8枚と同一)
    S = shape_xy(X, Y, Lx, Wy)
    Smax = float(S.max())

    # gain calibration（8枚と同一思想：shape最大点で +30V(rising) を 500nm に合わせる）
    raw_u0_nm = uz_abs_nm_from_V(+Vmax, loop, branch="up")
    raw_peak_nm = raw_u0_nm * Smax
    if raw_peak_nm <= 0:
        G = 1.0
        print("WARN: raw peak <= 0, gain=1.0")
    else:
        G = TARGET_PEAK_NM / raw_peak_nm
    print(f"Raw peak (+{Vmax:.0f}V rising @ shape-max) = {raw_peak_nm:.3f} nm")
    print(f"Mechanical gain G = {G:.3f} -> target peak {TARGET_PEAK_NM:.1f} nm")

    # =========================
    # Drive sequence (V only)
    # 1 cycle: rising: -30 -> -15 -> Vc(up) -> 0 -> +15 -> +30
    #          falling:+30 -> +15 -> Vc(down) -> 0 -> -15 -> -30
    # =========================
    keys_one_cycle = [
        -Vmax, -Vmid, Vc_up, 0.0, +Vmid, +Vmax,
        +Vmid, Vc_down, 0.0, -Vmid, -Vmax
    ]
    V_one = make_path_from_keys(keys_one_cycle, N_SEG)

    # repeat cycles（頭の重複を避ける）
    V_seq = [V_one]
    for _ in range(n_cycles - 1):
        V_seq.append(V_one[1:])
    V_seq = np.concatenate(V_seq)

    # =========================
    # Display settings (8枚と統一)
    # =========================
    cmap = mpl.colormaps["viridis"]
    norm = Normalize(vmin=0.0, vmax=UZ_MAX_NM)

    # zlim（真値0..500nm を、描画Z_EXAG込みの µm に変換）
    zmax_plot_um = (UZ_MAX_NM / 1000.0) * Z_EXAG
    tick_nm = [0, 250, 500]
    tick_um_plot = [(t / 1000.0) * Z_EXAG for t in tick_nm]

    frames: list[Image.Image] = []

    for i, V in enumerate(V_seq):
        V_prev = V_seq[i - 1] if i > 0 else V_seq[0]
        V_next = V_seq[i + 1] if i < len(V_seq) - 1 else None
        branch = pick_branch_by_slope(V_prev, V, V_next)

        # ABSOLUTE uz(V) (nm)
        u0_nm = uz_abs_nm_from_V(float(V), loop, branch=branch) * G
        U_nm = (u0_nm * S)
        if POSITIVE_ONLY:
            U_nm = np.clip(U_nm, 0.0, None)

        # 描画Z（nm->µm、さらにZ_EXAG倍）
        Z_plot_um = (U_nm / 1000.0) * Z_EXAG
        facecolors = cmap(norm(U_nm))

        fig = plt.figure(figsize=(6.2, 4.8))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot_surface(
            X_um, Y_um, Z_plot_um,
            facecolors=facecolors,
            linewidth=0,
            antialiased=True,
            shade=False,
        )

        # 軸
        ax.set_xlabel("x [µm]")
        ax.set_ylabel("y [µm]")
        ax.set_xlim(0, Lx * 1e6)
        ax.set_ylim(0, Wy * 1e6)

        ax.set_zlim(0.0, zmax_plot_um)
        ax.set_zticks(tick_um_plot)
        ax.set_zticklabels([str(t) for t in tick_nm])
        ax.set_zlabel("uz [nm]")

        # aspect（効く環境では y/x 比を保持）
        try:
            ax.set_box_aspect((1.0, (Wy / Lx), 0.35))
        except Exception:
            pass

        ax.view_init(elev=VIEW_ELEV, azim=VIEW_AZIM)

        # タイトル（V–I表記を含める）
        branch_str = "rising" if branch == "up" else "falling"
        fig.suptitle(
            "d33-dominated uz(x,y) (positive-only) | ABSOLUTE uz(V) consistent with butterfly\n"
            f"S=d33*(P/Pm)*E + Q*P^2 | Color: 0–{UZ_MAX_NM:.0f} nm | z(true): 0–{UZ_MAX_NM:.0f} nm | Z_EXAG={Z_EXAG:.0f}\n"
            f"V–I: current I not modeled | frame {i+1}/{len(V_seq)} | Vtop={V:+.2f} V ({branch_str})",
            fontsize=9.5,
        )

        # tight_layout は警告を出しやすいので避け、余白を固定
        fig.subplots_adjust(left=0.00, right=1.00, bottom=0.00, top=0.78)

        # frame capture
        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)[..., :3]
        img = Image.fromarray(buf, "RGB").convert("P", palette=Image.ADAPTIVE)
        frames.append(img)

        plt.close(fig)

    # save gif
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=110,  # ms
        loop=0,
        optimize=True,
    )

    print(f"Saved: {gif_path.resolve()}")


if __name__ == "__main__":
    main()
