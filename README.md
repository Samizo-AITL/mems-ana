# 🧩 mems-ana  
**Lightweight MEMS structural analysis tools (pre-FEM)**

`mems-ana` is a lightweight toolkit for **pre-FEM shape sanity checks** of MEMS structures,  
focused on **d33-dominant piezoelectric (PZT) actuation**.

This page is a **visual entry point**.  
For design intent and assumptions, see the repository README.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/mems-ana/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/mems-ana/tree/main) |

---

## 👀 What is shown here

- 📈 Out-of-plane displacement `uz(x, y)`  
- ⚡ d33-dominant actuation with simplified ferroelectric hysteresis  
- 🔌 **Voltage-driven analysis only**
  - Current **I is NOT modeled**
- 📐 Absolute displacement visualization  
  *(offset at 0 V is allowed)*

This is **not FEM**.  
It is used *before FEM* to check **shape**, **symmetry**, and **trend consistency**.

---

## ▶ Demo animation (recommended)

**d33-dominant uz(x, y), 10 voltage cycles**

- ➕ positive-only `uz`  
- 🎨 color / z-range fixed: **0–500 nm**  
- 📏 geometric aspect ratio preserved  
- 🔁 rising / falling branches included  

![](mems-ana_demo/outputs/anims/uz_midplane_typical_d33_10cycles.gif)

---

## 🖼 Static reference plots

Representative static results from the same model assumptions.

<img src="https://raw.githubusercontent.com/Samizo-AITL/mems-ana/main/mems-ana_demo/outputs/figs/uz_midplane_static8_d33_matchButterflyAbs_fixed0to500nm_ZEXAG.png" width="80%">

---

## 🧮 Modeling assumptions (explicit)

- Constitutive relation *(simplified)*:
  - `S(E) = d33 * (P/Pm) * Ez + Q * P(Ez)^2`
  - `uz ≈ S(E) * t_pzt`
- 🔄 P(E) includes up/down branches *(hysteresis)*  
- 📐 Absolute displacement is used *(no zero-shift correction)*  
- 🎯 This model prioritizes **shape consistency**, not material accuracy  

---

## 📸 Demo snapshot policy

All figures and animations shown here come from:

```
mems-ana_demo/
```

This directory is intentionally **frozen**:

- 🔒 no refactor  
- 🔒 no dependency update  
- 📌 used as a reproducible reference snapshot  

🔗 **GitHub Pages**  
[**/mems-ana_demo/**](https://samizo-aitl.github.io/mems-ana/mems-ana_demo/)

🔗 **GitHub (source)**  
[**/mems-ana_demo**](https://github.com/Samizo-AITL/mems-ana/tree/main/mems-ana_demo)

---

## 🧩 Design Core (ROM)

For **design-oriented analysis (not visualization)**,  
this project provides a calibrated **Reduced Order Model (ROM)**.

### mems-ana_core

- 🧱 Plate + piezo unimorph ROM  
- 📊 Pre-FEM frequency response and displacement analysis  
- 🧪 Shape factor **K_W** calibrated and contract-tested with pytest  

🔗 **GitHub Pages**  
[**/mems-ana_core/**](https://samizo-aitl.github.io/mems-ana/mems-ana_core/)

🔗 **GitHub (source)**  
[**/mems-ana_core**](https://github.com/Samizo-AITL/mems-ana/tree/main/mems-ana_core)

---

## 👤 Author

| 📌 Item | Details |
|--------|---------|
| **Name** | Shinichi Samizo |
| **Expertise** | Semiconductor devices (logic, memory, high-voltage mixed-signal)<br>Thin-film piezo actuators for inkjet systems<br>PrecisionCore printhead productization, BOM management, ISO training |
| **GitHub** | [![GitHub](https://img.shields.io/badge/GitHub-Samizo--AITL-blue?style=for-the-badge&logo=github)](https://github.com/Samizo-AITL) |

---

## 📄 License

[![Hybrid License](https://img.shields.io/badge/license-Hybrid-blueviolet)](https://samizo-aitl.github.io/mems-ana/#---license)

| 📌 Item | License | Description |
|--------|---------|-------------|
| **Source Code** | [**MIT License**](https://opensource.org/licenses/MIT) | Free to use, modify, and redistribute |
| **Text Materials** | [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/) or [**CC BY-SA 4.0**](https://creativecommons.org/licenses/by-sa/4.0/) | Attribution required; share-alike applies for BY-SA |
| **Figures & Diagrams** | [**CC BY-NC 4.0**](https://creativecommons.org/licenses/by-nc/4.0/) | Non-commercial use only |
| **External References** | Follow the original license | Cite the original source properly |

---

## 💬　Feedback

> Suggestions, improvements, and discussions are welcome via GitHub Discussions.

[![💬 GitHub Discussions](https://img.shields.io/badge/💬%20GitHub-Discussions-brightgreen?logo=github)](https://github.com/Samizo-AITL/mems-ana/discussions)


