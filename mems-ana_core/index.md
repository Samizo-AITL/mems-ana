---
title: "mems-ana_core | Calibrated MEMS Plate ROM"
layout: default
---

# mems-ana_core

**mems-ana_core** is a calibrated **Reduced Order Model (ROM)** for  
rectangular MEMS diaphragms with Si + PZT unimorph actuation.

It is designed for **pre-FEM analysis** and enables consistent evaluation of:

- Natural frequencies
- Frequency response functions (FRF)
- Center displacement
- Electrical terminal behavior (V–I)

within a single, physically consistent framework.

---

## Key Features

- 📐 Kirchhoff–Love plate theory
- ⚡ Piezo eigenstrain → bending moment → curvature → displacement
- 🔁 Modal superposition–based FRF
- 🧪 Physics-level contract tests using `pytest`
- 🧊 Shape factor **K_W** treated as a 1-point calibrated parameter

---

## Calibration Policy (Important)

This ROM introduces a **shape factor `K_W`** that aggregates:

- Plate geometry
- Boundary conditions
- Mode shape normalization

The policy is:

- `K_W` is calibrated at **one reference point** (FEM or measurement)
- After calibration, `K_W` acts as a **pure linear scaling factor**
- Electrical quantities are **independent of `K_W`**

This behavior is guaranteed by the following test:

```text
mems_ana/tests/test_kw_scaling.py
```

---

## Intended Use Cases

- Early-stage MEMS diaphragm design
- Order-of-magnitude and sensitivity analysis before FEM
- Educational and analysis templates
- Control-oriented frequency/Q estimation

---

## Directory Structure (Excerpt)

```text
mems-ana_core/
├─ mems_ana/
│  ├─ geometry/
│  ├─ materials/
│  ├─ physics/
│  ├─ rom/
│  ├─ solver/
│  └─ tests/
├─ pyproject.toml
├─ README.md
└─ CHANGELOG.md
```

---

## Status

- ✔ ROM structure finalized
- ✔ K_W calibration completed
- ✔ Tests passing
- ✔ Published on GitHub

**This module is frozen as a design-ready ROM.**
