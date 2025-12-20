## Current Status (YYYY-MM-DD)

- Rectangular MEMS diaphragm ROM (plate + piezo unimorph)
- Laminate-based bending stiffness D implemented
- Piezo eigenstrain → bending moment → curvature → center displacement
- Modal analysis + FRF (center uz) + terminal V–I are consistent

### Verified Conditions
- Plate: 1.5 mm × 1.5 mm
- Stack: Si 8 µm + PZT 2 µm
- Drive: 10 Vrms
- Result:
  - (1,1) mode ≈ 48 kHz
  - uz_peak ≈ 5e-15 m (before K_W calibration)
  - I ≈ 24 mA

### Known Simplifications
- Piezo elastic constants (E, nu) not yet separated from base
- Shape factor K_W requires 1-point calibration (FEM or measurement)
