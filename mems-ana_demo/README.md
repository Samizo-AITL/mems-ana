# mems-ana_demo

This directory is a **frozen demo snapshot**.

- Purpose: Reproduce d33-dominant uz(x,y) visualization with hysteresis
- Scope: V-only analysis (current I is NOT modeled)
- Status: Stable / no refactor planned

## How to run
```powershell
python -m pip install -e .
python examples/animate_uz_midplane_typical_d33.py
```

## Notes

ABSOLUTE displacement (offset at 0V allowed)
Visualization scale fixed: 0–500 nm