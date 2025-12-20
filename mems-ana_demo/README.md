# mems-ana_demo

This directory contains a **frozen demo snapshot** for visualizing
**d33-dominant MEMS piezoelectric behavior** driven by a
**ferroelectric P–Ez hysteresis loop**.

The demo is designed to be **stable, reproducible, and explanatory**,
serving as a reference for how electrical hysteresis maps into
mechanical displacement fields.

---

## Overview

- Electrical input: **P–Ez hysteresis (voltage-driven only)**
- Mechanical output: **out-of-plane displacement $u_z(x,y)$**
- Dominant coupling: **piezoelectric $d_{33}$**
- Analysis type: **quasi-static**
- Purpose: **visualization and conceptual understanding**

This demo is **not** intended for quantitative device optimization.

---

## 1. Electrical input: P–Ez hysteresis
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/pzt_pe_hysteresis_1d.png" width="80%">

This figure defines the **polarization–electric field hysteresis loop**
used as the sole electrical input.

- Voltage-driven analysis (**V-only**)
- Electrical current $I$ is **not modeled**
- Rising and falling branches are explicitly defined by the loop

All subsequent mechanical results are derived consistently from this input.

---

## 2. uz–V butterfly response (d33-dominant)
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/uz_butterfly_d33_hyst_scaled_0to500nm.png" width="80%">

This plot shows the **butterfly-shaped displacement–voltage relation**.

- Vertical axis: absolute displacement $u_z$
- Horizontal axis: applied voltage
- Response is dominated by **$d_{33}$ coupling**
- Visualization scale is **fixed to 0–500 nm**

The butterfly shape directly reflects the underlying P–Ez hysteresis.

---

## 3. Static mid-plane displacement maps
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/uz_midplane_static8_d33_matchButterflyAbs_fixed0to500nm_ZEXAG.png" width="80%">

These images show **spatial distributions of $u_z(x,y)$** at the MEMS
mid-plane for selected voltage points.

- Displacement is treated as **ABSOLUTE $u_z$**
- Offset at 0 V is allowed
- Mechanical boundary conditions are **schematic**
- All frames share the same color scale (0–500 nm)

This enables direct visual comparison across voltage states.

---

## 4. Dynamic visualization over voltage cycles
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/anims/uz_midplane_typical_d33_10cycles.gif" width="80%">

This animation shows the **evolution of $u_z(x,y)$** over multiple voltage cycles.

- Voltage follows the P–Ez hysteresis loop
- Quasi-static response (no inertia, no damping)
- Intended for **intuitive understanding**, not transient accuracy

---

## Directory structure
```
mems-ana_demo/
├─ examples/        # demo and animation scripts
├─ outputs/
│  ├─ figs/         # static figures (PNG)
│  └─ anims/        # animations (GIF)
├─ README.md
└─ index.md
```

---

## How to run
```bash
python -m pip install -e .
python examples/animate_uz_midplane_typical_d33.py
```

---

## Scope and limitations
- Voltage-driven only (current not modeled)
- d33-dominant piezoelectric coupling
- No electrical losses
- No nonlinear elasticity
- No realistic anchor or package constraints

These simplifications are intentional to keep the demo clear and stable.

---

## Status
- **Stable**
- Frozen demo snapshot
- No refactor planned
- Parameters fixed for reproducibility

---

## Disclaimer
This demo is provided for **conceptual visualization and documentation**.
Real MEMS device design and quantitative evaluation require
additional physics, including current flow, losses,
nonlinear mechanics, and realistic boundary conditions.
