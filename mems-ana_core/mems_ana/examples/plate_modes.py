from mems_ana.geometry.plate import RectPlate
from mems_ana.materials.elastic import IsoElastic
from mems_ana.materials.piezo import PiezoMat
from mems_ana.materials.stack import Stack
from mems_ana.rom.plate_rom import RectPlateROM, Mode

plate = RectPlate(a=1.5e-3, b=1.5e-3)
si = IsoElastic(E=160e9, nu=0.22, rho=2330.0)
pzt = PiezoMat(d31=-120e-12, eps_r=1000.0, tan_delta=0.02)

stack = Stack(base=si, t_base=8e-6, piezo=pzt, t_pzt=2e-6, elec_area_ratio=0.8)

model = RectPlateROM(plate, stack, modes=[
    Mode(1,1), Mode(2,1), Mode(1,2), Mode(2,2), Mode(3,1), Mode(1,3)
])

print("Modal frequencies [Hz] (approx, clamped-corrected):")
for k, f in model.modal_freqs_hz().items():
    print(f"{k}: {f:,.0f} Hz")
