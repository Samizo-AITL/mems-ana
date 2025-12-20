---
title: mems-ana_demo
description: d33-dominant MEMS piezoelectric hysteresis visualization (frozen demo snapshot)
---

# mems-ana_demo  
**d33-dominant MEMS piezoelectric hysteresis visualization**

This directory contains a **frozen demo snapshot** that visualizes the quasi-static
out-of-plane displacement of a MEMS piezoelectric structure dominated by the
piezoelectric coefficient **d33**, driven by a ferroelectric **P–Ez hysteresis loop**.

The purpose of this demo is **not quantitative device design**, but to provide a
clear, reproducible reference showing how electrical hysteresis maps into
mechanical displacement patterns.

---

## 1. Electrical input: P–Ez hysteresis (V-only)
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/pzt_pe_hysteresis_1d.png" width="80%">

This figure shows the **polarization–electric field (P–Ez) hysteresis loop**
used as the electrical input to the model.

- The analysis is **voltage-driven only**
- Electrical current and dynamic switching effects are **not modeled**
- The closed loop defines the rising and falling voltage branches consistently

This hysteresis is imposed as a fixed input condition for all subsequent results.

---

## 2. uz–V butterfly curve (d33-dominant, fixed scale)
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/uz_butterfly_d33_hyst_scaled_0to500nm.png" width="80%">

This plot shows the resulting **butterfly-shaped displacement–voltage response**
derived from the P–Ez hysteresis under a **d33-dominant assumption**.

- Vertical axis: out-of-plane displacement $u_z$
- Horizontal axis: applied voltage
- Visualization scale is **fixed to 0–500 nm**

The butterfly shape directly reflects the underlying ferroelectric hysteresis.

---

## 3. Static uz(x,y) mid-plane maps (absolute displacement)
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/uz_midplane_static8_d33_matchButterflyAbs_fixed0to500nm_ZEXAG.png" width="80%">

These snapshots show the **spatial distribution of $u_z(x,y)$** at the MEMS
mid-plane for selected voltage points along the butterfly curve.

- Displacement is treated as **ABSOLUTE $u_z$**
- An offset at 0 V is allowed
- Mechanical boundary conditions are **schematic / conceptual**

All frames use the **same color scale (0–500 nm)** to allow direct comparison.

---

## 4. Dynamic response: uz(x,y) over voltage cycles
<img src="http://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/anims/uz_midplane_typical_d33_10cycles.gif" width="80%">

This animation shows the **time evolution of $u_z(x,y)$** over multiple voltage
cycles following the hysteresis loop.

- Rising and falling branches follow the P–Ez loop
- The response is quasi-static (no inertia or damping modeled)
- Intended for **intuitive understanding**, not transient accuracy

---

## How to run
```bash
python -m pip install -e .
python examples/animate_uz_midplane_typical_d33.py
```

---

## Scope and limitations
- Voltage-driven analysis only (current not modeled)
- d33-dominant piezoelectric response
- No losses, no nonlinear elasticity, no realistic anchors
- Boundary conditions are simplified for clarity

---

## Status
- **Stable**
- Frozen demo snapshot
- Parameters are fixed to ensure reproducibility

---

## Disclaimer
This demo is intended for **conceptual understanding and visualization**.
Real device design and quantitative evaluation require additional physics,
including electrical current, losses, nonlinear mechanics, and realistic
boundary conditions.
