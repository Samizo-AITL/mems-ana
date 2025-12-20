# -*- coding: utf-8 -*-
"""
ferroelectric.py

Purpose:
- "形を見る" ための簡易 P–E ヒステリシス生成
- rising/falling 枝と、閉ループ列を返す

Notes:
- これは材料モデルの厳密解ではありません。
- Pr_target を指定して、tanh の平滑係数 Es を自動決定します。
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def _solve_Es_from_Pr(Pm: float, Pr_target: float, Ec: float) -> float:
    """
    Pr_target / Pm = tanh(Ec / Es) を満たす Es を計算します。
    tanh^{-1}(r) = 0.5 ln((1+r)/(1-r))
    """
    r = Pr_target / Pm
    if abs(r) >= 1.0:
        raise ValueError("Pr_target must satisfy |Pr_target| < Pm.")

    arctanh_r = 0.5 * np.log((1.0 + r) / (1.0 - r))
    # Ec/Es = arctanh(r) → Es = Ec / arctanh(r)
    return Ec / arctanh_r


def make_branches(
    E_V_per_m: np.ndarray,
    *,
    Ec_V_per_m: float,
    Es_V_per_m: float,
    Pm_uC_cm2: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    rising/falling 枝を生成します。

    P_up(E)   = Pm * tanh((E + Ec)/Es)
    P_down(E) = Pm * tanh((E - Ec)/Es)

    返り値:
      (P_up_uC_cm2, P_down_uC_cm2)
    """
    E = np.asarray(E_V_per_m, dtype=float)
    Ec = float(Ec_V_per_m)
    Es = float(Es_V_per_m)
    Pm = float(Pm_uC_cm2)

    P_up = Pm * np.tanh((E + Ec) / Es)
    P_dn = Pm * np.tanh((E - Ec) / Es)

    # 端点の ±Pm を揃える（見た目の対称性を保つ）
    P_pos = 0.5 * (np.max(P_up) + np.max(P_dn))
    P_neg = 0.5 * (np.min(P_up) + np.min(P_dn))

    def _scale(P: np.ndarray) -> np.ndarray:
        P = P.copy()
        pos_mask = P >= 0
        if np.any(pos_mask):
            P[pos_mask] *= (P_pos / np.max(P[pos_mask]))
        neg_mask = ~pos_mask
        if np.any(neg_mask):
            P[neg_mask] *= (P_neg / np.min(P[neg_mask]))
        return P

    return _scale(P_up), _scale(P_dn)


def make_closed_loop(
    E_V_per_m: np.ndarray,
    *,
    Ec_V_per_m: float,
    Pm_uC_cm2: float,
    Pr_target_uC_cm2: float,
    Es_V_per_m: float | None = None,
    n_jump: int = 120,
) -> dict[str, np.ndarray | float]:
    """
    P–E の閉ループ（表示用）を作ります。

    入力:
      E_V_per_m: -Emax → +Emax の単調配列（推奨）
      Ec, Pm, Pr_target: 形状パラメータ
      Es: None の場合、Pr_target から自動決定
      n_jump: 右端・左端の “ジャンプ” 点数（閉ループ化のため）

    出力(dict):
      - P_up_uC_cm2, P_down_uC_cm2
      - Eloop_V_per_m, Ploop_uC_cm2（閉ループの連結列）
      - Es_V_per_m
      - Pr_rising_uC_cm2, Pr_falling_uC_cm2（E≈0の値）
    """
    E = np.asarray(E_V_per_m, dtype=float)
    if E.ndim != 1:
        raise ValueError("E_V_per_m must be 1D array.")

    Ec = float(Ec_V_per_m)
    Pm = float(Pm_uC_cm2)
    Prt = float(Pr_target_uC_cm2)

    if Es_V_per_m is None:
        Es = _solve_Es_from_Pr(Pm=Pm, Pr_target=Prt, Ec=Ec)
    else:
        Es = float(Es_V_per_m)

    P_up, P_dn = make_branches(E, Ec_V_per_m=Ec, Es_V_per_m=Es, Pm_uC_cm2=Pm)

    # Pr（E≈0）
    idx0 = int(np.argmin(np.abs(E)))
    Pr_r = float(P_up[idx0])
    Pr_f = float(P_dn[idx0])

    # 閉ループを構成：左→右 (rising) → 右端ジャンプ → 右→左 (falling) → 左端ジャンプ
    E1, P1 = E, P_up

    Ej1 = np.full(n_jump, E[-1], dtype=float)
    Pj1 = np.linspace(P_up[-1], P_dn[-1], n_jump)

    E2, P2 = E[::-1], P_dn[::-1]

    Ej2 = np.full(n_jump, E[0], dtype=float)
    Pj2 = np.linspace(P_dn[0], P_up[0], n_jump)

    Eloop = np.concatenate([E1, Ej1, E2, Ej2])
    Ploop = np.concatenate([P1, Pj1, P2, Pj2])

    return {
        "P_up_uC_cm2": P_up,
        "P_down_uC_cm2": P_dn,
        "Eloop_V_per_m": Eloop,
        "Ploop_uC_cm2": Ploop,
        "Es_V_per_m": float(Es),
        "Pr_rising_uC_cm2": Pr_r,
        "Pr_falling_uC_cm2": Pr_f,
    }
