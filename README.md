# mems-ana

**Pre-FEM MEMS structural analysis toolkit for fast design exploration.**

**mems-ana** enables rapid, lightweight evaluation of MEMS structural responses  
driven by **boundary condition × geometry × electrical drive**,  
*before* committing to full FEM or TCAD simulations.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/mems-ana/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/mems-ana/tree/main) |

---

## What This Is

- **Pre-FEM / pre-TCAD structural analysis**
- Fast comparison of **stress distributions and trends**
- Design-stage insight, not high-fidelity accuracy
- Intended for **engineers making early design decisions**

---

## Scope

### In Scope
- MEMS structural stress / strain evaluation
- PZT-driven and thin-film layered structures
- 2D and reduced-order analytical models
- Voltage, geometry, and boundary-condition sweeps
- Visualization for design review (maps, curves, animations)

### Out of Scope
- High-accuracy FEM correlation
- Full process or material nonlinearity
- Circuit, control, or system-level simulation
- Time-dependent hysteresis or dynamics (unless explicitly added)

---

## Typical Use Cases

- Estimating stress scaling with applied voltage
- Comparing boundary conditions and anchor designs
- Screening geometries before FEM
- Identifying stress concentration regions
- Generating figures for design reviews and discussions

---

## Directory Structure

```text
mems-ana/
├─ src/        # core analytical models
├─ examples/   # representative use cases (PZT, arch, BC comparison)
├─ figs/       # output figures and animations
├─ docs/       # analysis items, assumptions, scaling notes
└─ README.md
```

---

## Design Philosophy

- **Fast over perfect**
- **Relative comparison over absolute accuracy**
- **Insight over completeness**
- **FEM is a downstream tool, not the starting point**

---

## Status

Work in progress.  
Models, APIs, and directory structure may evolve as the design space expands.

---

*mems-ana is built to answer one question efficiently:*  
**“Which designs are worth running FEM on next?”**

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


