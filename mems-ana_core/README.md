# mems-ana_core

Calibrated **Reduced Order Model (ROM)** for MEMS rectangular plates  
with piezoelectric unimorph actuation.

---

## Overview

`mems-ana_core` is a lightweight analysis core for MEMS diaphragms  
composed of a silicon substrate and a PZT thin film.

It provides a unified model for:

- Natural frequencies
- Center displacement FRF
- Piezoelectric terminal current (V–I)

targeted at **pre-FEM design stages**.

---

## Core Design Principles

### 1. Shape Factor `K_W`

- `K_W` aggregates geometry, boundary conditions, and modal shape effects
- It is calibrated using **a single reference point**
- After calibration, it acts only as a **linear scaling factor**

This linearity is enforced by a pytest contract test:

```text
mems_ana/tests/test_kw_scaling.py
```

---

### 2. Electrical–Mechanical Separation

- Electrical quantities (capacitance, loss, current)  
  do **not** depend on `K_W`
- Mechanical displacement scales linearly with `K_W`

---

## Example Usage

```bash
python -m mems_ana.examples.plate_static
python -m mems_ana.examples.plate_frf_vi
```

---

## Testing

```bash
pytest mems_ana/tests
```

All tests must pass to guarantee physical consistency  
and API-level contracts of the ROM.

---

## Intended Applications

- Early MEMS structural design
- Pre-FEM scaling and sensitivity studies
- Educational and reference implementations
- Control bandwidth and Q-factor estimation

---

## Status

- ✔ ROM: complete
- ✔ Calibration: complete
- ✔ Tests: PASS
- ✔ GitHub: published

This module is **frozen as a design-grade analysis core**.
