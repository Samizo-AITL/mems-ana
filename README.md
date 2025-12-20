# mems-ana

**Lightweight MEMS structural analysis tools (pre-FEM)**

`mems-ana` is a lightweight Python-based toolkit for **pre-FEM shape sanity checks** of MEMS structures,  
with a focus on **piezoelectric (PZT) d33-dominant actuation**.

This repository prioritizes **physical consistency and interpretability** over numerical completeness.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/mems-ana/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/mems-ana/tree/main) |

---

## What this repository is

- Pre-FEM analysis tools to **inspect displacement shape and trends**
- d33-dominant out-of-plane displacement `uz(x, y)`
- Simplified ferroelectric hysteresis modeling (P–Ez)
- **Voltage-driven analysis only**
  - Electric current **I is NOT modeled**
- Absolute displacement visualization (offset at 0 V is allowed)

This project is **not a FEM replacement**.  
It is intended to be used *before* FEM for design intuition and sanity checking.

---

## What this repository is NOT

- ❌ Full multiphysics FEM
- ❌ Electrical current / charge transport model
- ❌ Device-level performance predictor
- ❌ Material-accurate PZT database

---

## Demo snapshot (recommended entry point)

A **frozen, reproducible demo snapshot** is provided here:

```
mems-ana_demo/
```

Contents:
- d33-dominant `uz(x, y)` visualization
- P–Ez hysteresis loop
- u–V butterfly curve
- Static 8-panel midplane plots
- 10-cycle animation GIF (absolute uz, positive-only)

⚠️ **Policy**  
`mems-ana_demo/` is intentionally **frozen**.
- No refactor
- No dependency update
- Used as a reference snapshot only

If you want to understand what this project does, **start here**.

---

## Repository structure

```
mems-ana/
├─ mems-ana_demo/        # frozen demo snapshot (reference)
│  ├─ examples/
│  ├─ outputs/
│  │  ├─ figs/
│  │  └─ anims/
│  └─ src/mems_ana/
│
├─ src/mems_ana/         # reusable core logic (evolving)
│  └─ ferroelectric.py
│
├─ examples/             # future / experimental scripts
├─ assets/               # GitHub Pages assets
├─ index.md              # GitHub Pages entry
└─ README.md             # this file
```

---

## Physical assumptions (explicit)

- d33-dominant strain model
- Simplified constitutive relation:
  - `S(E) = d33 * (P/Pm) * Ez + Q * P(Ez)^2`
  - `uz ≈ S(E) * t_pzt`
- P(E) uses up/down branches (hysteresis)
- Display conventions:
  - positive-only `uz` (negative clipped)
  - fixed color and z-range: **0–500 nm**
  - geometric aspect ratio preserved

---

## License / usage

This repository is intended for **research, education, and design exploration**.

If you reuse ideas or figures, please cite appropriately.

---

## Status

- Core concept: **stable**
- Demo snapshot: **frozen**
- Refactor / extension: **future work**

---

*Author: Shinichi Samizo*  
*Project: mems-ana*
