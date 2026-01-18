---
layout: default
title: mems-ana_core
permalink: /mems-ana_core/
---

# 🧠 mems-ana_core

**mems-ana_core** is a calibrated **Reduced Order Model (ROM)** for  
rectangular MEMS diaphragms with **Si + PZT unimorph actuation**.

It is designed explicitly for **pre-FEM analysis**, providing a compact but  
physically consistent framework to evaluate:

- 🟦 Natural frequencies
- 📈 Frequency response functions (FRF)
- 📍 Center displacement
- ⚡ Electrical terminal behavior (V–I)

—all within a **single, unified electromechanical model**.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/mems-ana/mems-ana_core/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/mems-ana/tree/main/mems-ana_core) |

---

## ✨ Key Features

- 📐 **Kirchhoff–Love plate theory**–based formulation
- ⚡ Piezoelectric eigenstrain  
  → bending moment → curvature → displacement
- 🔁 **Modal superposition–based FRF** evaluation
- 🧪 Physics-level **contract tests** using `pytest`
- 🧊 Shape factor **`K_W`** treated as a *single-point calibrated parameter*

---

## 🎯 Calibration Policy (Important)

This ROM introduces a **shape factor `K_W`**, which aggregates the effects of:

- Plate geometry
- Mechanical boundary conditions
- Mode shape normalization

### Calibration rules

- `K_W` is calibrated at **one reference operating point**  
  (from FEM or experimental measurement)
- After calibration, `K_W` acts as a **pure linear scaling factor**
- **Electrical quantities (V–I)** are **strictly independent of `K_W`**

This separation is **explicitly enforced and verified** by the following test:

```text
mems_ana/tests/test_kw_scaling.py
```

✅ This guarantees **mechanical scaling without electrical contamination**.

---

## 🧭 Intended Use Cases

- Early-stage MEMS diaphragm design
- Order-of-magnitude and sensitivity studies prior to FEM
- Educational and analysis reference models
- Control-oriented resonance / Q-factor estimation

---

## 📁 Directory Structure (Excerpt)

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

## 🧊 Status

- ✔ ROM structure finalized
- ✔ `K_W` calibration completed
- ✔ All tests passing
- ✔ Published on GitHub

**This module is frozen as a design-ready ROM.**
