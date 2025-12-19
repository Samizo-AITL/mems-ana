# mems-ana

**Lightweight MEMS structural analysis tools (pre-FEM).**

This repository provides lightweight analytical tools for **design-stage MEMS structural analysis**.  
It focuses on fast evaluation of structural responses driven by:

**boundary condition × geometry × drive**

The primary use case is **pre-FEM / pre-TCAD design exploration**, not high-fidelity simulation.

---

## Scope

- Structural stress / strain analysis for MEMS
- Simplified models including PZT and thin-film layers
- 2D and reduced-order analytical approaches
- Fast parameter sweep for early design decisions

**Out of scope:**

- High-accuracy FEM
- Full process or material nonlinearity modeling
- Circuit or control simulation

---

## Typical Use Cases

- Estimating stress scaling with applied voltage
- Comparing boundary conditions and geometries
- Identifying critical regions before FEM
- Generating figures for design reviews

---

## Directory Structure

```text
mems-ana/
├─ src/        # core analytical models
├─ examples/   # PZT, arch, and boundary-condition examples
├─ figs/       # output figures
└─ README.md
```

---

## Status

Work in progress.  
APIs, models, and directory structure may change.

---

## Philosophy

- **Fast over perfect**
- **Insight over completeness**
- **Design-stage first**

---
