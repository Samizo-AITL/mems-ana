---
layout: default
title: mems-ana
---

# mems-ana  
**Lightweight MEMS structural analysis tools (pre-FEM)**

`mems-ana` is a lightweight toolkit for **pre-FEM shape sanity checks** of MEMS structures,  
focused on **d33-dominant piezoelectric (PZT) actuation**.

This page is a **visual entry point**.  
For design intent and assumptions, see the repository README.

---

## What is shown here

- Out-of-plane displacement `uz(x, y)`
- d33-dominant actuation with simplified ferroelectric hysteresis
- **Voltage-driven analysis only**
  - Current **I is NOT modeled**
- Absolute displacement visualization  
  (offset at 0 V is allowed)

This is **not FEM**.  
It is used *before FEM* to check shape, symmetry, and trend consistency.

---

## Demo animation (recommended)

**d33-dominant uz(x, y), 10 voltage cycles**

- positive-only `uz`
- color / z-range fixed: **0–500 nm**
- geometric aspect ratio preserved
- rising / falling branches included

![](mems-ana_demo/outputs/anims/uz_midplane_typical_d33_10cycles.gif)

---

## Static reference plots

Representative static results from the same model assumptions.

![](mems-ana_demo/outputs/figs/uz_midplane_static8_d33_matchButterfly.png)

---

## Modeling assumptions (explicit)

- Constitutive relation (simplified):
  - `S(E) = d33 * (P/Pm) * Ez + Q * P(Ez)^2`
  - `uz ≈ S(E) * t_pzt`
- P(E) includes up/down branches (hysteresis)
- Absolute displacement is used (no zero-shift correction)
- This model prioritizes **shape consistency**, not material accuracy

---

## Demo snapshot policy

All figures and animations shown here come from:

```
mems-ana_demo/
```

This directory is intentionally **frozen**:
- no refactor
- no dependency update
- used as a reproducible reference snapshot

---

## Repository

- GitHub: https://github.com/Samizo-AITL/mems-ana
- Demo snapshot: `mems-ana_demo/`
- Core logic: `src/mems_ana/`

---

# 👤 8.　Author

| 📌 Item | Details |
|--------|---------|
| **Name** | Shinichi Samizo |
| **Education** | M.S. in Electrical and Electronic Engineering, Shinshu University |
| **Career** | Former Engineer at Seiko Epson Corporation (since 1997) |
| **Expertise** | Semiconductor devices (logic, memory, high-voltage mixed-signal)<br>Thin-film piezo actuators for inkjet systems<br>PrecisionCore printhead productization, BOM management, ISO training |
| **Email** | [![Email](https://img.shields.io/badge/Email-shin3t72%40gmail.com-red?style=for-the-badge&logo=gmail)](mailto:shin3t72@gmail.com) |
| **X (Twitter)** | [![X](https://img.shields.io/badge/X-@shin3t72-black?style=for-the-badge&logo=x)](https://x.com/shin3t72) |
| **GitHub** | [![GitHub](https://img.shields.io/badge/GitHub-Samizo--AITL-blue?style=for-the-badge&logo=github)](https://github.com/Samizo-AITL) |

---

# 📄 9. License

[![Hybrid License](https://img.shields.io/badge/license-Hybrid-blueviolet)](https://samizo-aitl.github.io/mems-ana//#-license)

| Item | License | Description |
|------|---------|-------------|
| **Source Code** | MIT | Free to use, modify, redistribute |
| **Text Materials** | CC BY 4.0 / CC BY-SA 4.0 | Attribution & share-alike rules |
| **Figures & Diagrams** | CC BY-NC 4.0 | Non-commercial use |
| **External References** | Original license applies | Cite properly |

---

# 💬 10.　Feedback

> Suggestions, improvements, and discussions are welcome via GitHub Discussions.

[![💬 GitHub Discussions](https://img.shields.io/badge/💬%20GitHub-Discussions-brightgreen?logo=github)](https://github.com/Samizo-AITL/mems-ana/discussions)

