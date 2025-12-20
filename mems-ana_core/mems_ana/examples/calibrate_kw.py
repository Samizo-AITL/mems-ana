# examples/calibrate_kw.py

from mems_ana.rom.plate_rom import PlateROM
from mems_ana.io.config import KW_SHAPE

# === ここを自分で決める ===
UZ_REF = 1.0e-9   # FEM or 実測の中央変位 [m]
V_RMS  = 10.0     # 今まで使ってた電圧

# === ROM実行 ===
rom = PlateROM()
uz_rom = rom.static_response(V_RMS)

KW = UZ_REF / uz_rom

print("=== K_W calibration ===")
print("K_W =", KW)
