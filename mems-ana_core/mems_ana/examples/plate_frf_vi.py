import numpy as np
from mems_ana.geometry.plate import RectPlate
from mems_ana.materials.elastic import IsoElastic
from mems_ana.materials.piezo import PiezoMat
from mems_ana.materials.stack import Stack
from mems_ana.rom.plate_rom import RectPlateROM, Mode

plate = RectPlate(a=1.5e-3, b=1.5e-3)
si = IsoElastic(E=160e9, nu=0.22, rho=2330.0)
pzt = PiezoMat(d31=-120e-12, eps_r=1000.0, tan_delta=0.02)

stack = Stack(base=si, t_base=8e-6, piezo=pzt, t_pzt=2e-6, elec_area_ratio=0.8)

model = RectPlateROM(plate, stack, modes=[Mode(1,1), Mode(2,1), Mode(1,2), Mode(2,2)])

V_rms = 10.0
f_list = np.linspace(1e3, 200e3, 400)

uz_list = []
I_list = []

for f in f_list:
    uz, I = model.frf_center_uz_and_I(V_rms=V_rms, f_hz=float(f), zeta=0.02)
    uz_list.append(uz)
    I_list.append(I)

i_max = int(np.argmax(np.array(uz_list)))
print(f"Peak uz (rough) at f={f_list[i_max]:.0f} Hz : uz_peak={uz_list[i_max]:.3e} m")
print(f"At that f, terminal current (RMS): I={I_list[i_max]:.3e} A")
