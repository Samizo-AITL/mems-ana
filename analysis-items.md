---
title: mems-ana Analysis Items
lang: en
---

# 🧪 Analysis Parameters & Outputs (mems-ana)

This document summarizes **analysis parameters**, **parameter sweeps**, **evaluation metrics**,  
and **visualization/animation items** for the *pre-FEM MEMS structural analysis* workflow in **mems-ana**.

---

## 1. Drive Conditions（駆動条件）

### Electrical
- **Voltage difference**  
  $$ \Delta V = V_{\text{bottom}} - V_{\text{top}} $$
- Voltage levels (example): 0 / 15 / 30 V
- Polarity: $+\Delta V$, $-\Delta V$
- Electrode configuration:
  - Full coverage
  - Partial / segmented electrodes

### Derived
- Electric field  
  $$ E_z = \frac{\Delta V}{t_{\mathrm{PZT}}} $$

---

## 2. Geometry Parameters（形状パラメータ）

### Plate / Beam Geometry
- Length $L$
- Width $W$
- Thickness $t$
- Aspect ratio $L/W$

### PZT Layer
- PZT thickness $t_{\mathrm{PZT}}$
- Electrode coverage ratio
- Mid-plane vs offset placement

### Shape
- Flat plate
- Arch (curvature, rise height)
- Tapered / ribbed variants (optional)

---

## 3. Boundary Conditions（境界条件）

- All edges clamped
- All edges free
- Short edge clamped / long edge free
- Short edge clamped / long edge guided
- Cantilever
- Spring boundary (parametric):
  - Translational stiffness $k_z$
  - Rotational stiffness $k_\theta$

---

## 4. Material Parameters（材料パラメータ）

### Piezoelectric (PZT)
- Piezoelectric coefficient $d_{31}$
- Permittivity $\varepsilon$
- Elastic compliance $s^E$
- Optional bias dependence: $d_{31}(E)$ (no hysteresis)

### Structural Layers
- Young’s modulus $E$
- Poisson’s ratio $\nu$
- Residual stress $\sigma_0$

---

## 5. Environmental / Secondary Effects（任意）

- Fringe-field correction factor
- Substrate / environment potential (e.g. GND reference)
- Electrode resistance (voltage drop along electrode)
- Temperature offset (via residual stress)

---

## 6. Primary Field Outputs（分布出力）

- Stress field: $\sigma_{zz}(x,y)$
- Displacement field: $w(x,y)$ (if enabled)
- Strain field: $\varepsilon_{zz}(x,y)$

Visualization:
- 2D contour maps
- 3D surface plots
- Line cuts (centerline, edge, etc.)

---

## 7. Scalar Evaluation Metrics（評価指標）

Used for **design comparison and ranking**.

- Maximum stress  
  $$ \max(|\sigma_{zz}|) $$

- Average stress  
  $$ \mathrm{avg}(|\sigma_{zz}|) $$

- Stress concentration factor  
  $$ C = \frac{\max(|\sigma_{zz}|)}{\mathrm{avg}(|\sigma_{zz}|)} $$

- Area fraction above threshold  
  $$ \frac{\text{Area}(|\sigma_{zz}| > \sigma_{\mathrm{th}})}{\text{Total area}} $$

---

## 8. Typical Parameter Sweeps（代表的スイープ）

- Voltage sweep: $\Delta V$
- Geometry sweep: $L/W$, $t_{\mathrm{PZT}}$
- Boundary-condition comparison
- Material sensitivity: $d_{31} \pm 10\%$
- Electrode coverage ratio sweep

---

## 9. Voltage-Cycle Animation（準静的アニメーション）

### Purpose
Visualize **stress evolution under cyclic voltage drive** for design review and explanation.  
This is a **quasi-static visualization**, not a time-dependent dynamic simulation.

### Voltage Sequence
One cycle:
$$
0 \rightarrow 15 \rightarrow 30 \rightarrow 15 \rightarrow 0 \ \text{(V)}
$$

- Number of cycles: **10**
- Total frames: $5 \times 10 = 50$

### Notes
- No piezoelectric hysteresis included
- Identical voltage values produce identical stress fields
- Frame index is treated as *pseudo-time*

### Output
- Animated $\sigma_{zz}(x,y)$ heatmap
- Fixed color scale across all frames
- Voltage level and cycle index annotated

Example annotation:
```
ΔV = 30 V | cycle 4 / 10
```

### Recommended Formats
- **GIF** (GitHub Pages / documentation)
- **MP4** (presentation / review)

### Documentation Note
> *This animation represents a quasi-static voltage sweep for visualization purposes.  
> Time-dependent piezoelectric hysteresis and dynamic effects are not included.*

---

## 10. Design Philosophy (pre-FEM)

- **Fast over perfect**
- **Relative comparison over absolute accuracy**
- **Insight into scaling and trends**
- FEM and TCAD are applied *after* narrowing design candidates

---

*This document defines the analytical scope of **mems-ana** as a pre-FEM MEMS design exploration tool.*
