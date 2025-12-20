import math

from mems_ana.geometry.plate import RectPlate
from mems_ana.materials.stack import Stack
from mems_ana.materials.elastic import IsoElastic
from mems_ana.materials.piezo import PiezoMaterial
from mems_ana.rom.plate_rom import RectPlateROM


def make_test_rom(K_W: float) -> RectPlateROM:
    plate = RectPlate(a=1.5e-3, b=1.5e-3)

    si = IsoElastic(E=170e9, nu=0.28, rho=2330)
    pzt = PiezoMaterial(
        E=60e9,
        nu=0.31,
        rho=7500,
        eps_r=1200,
        d31=-180e-12,
        tan_delta=0.02,
    )

    # ★ Stack の正しい引数順 ★
    stack = Stack(
        si,     # substrate (Si)
        8e-6,   # t_si
        pzt,    # piezo material
        2e-6,   # t_pzt
        1.0,    # elec_area_ratio
    )

    return RectPlateROM(plate=plate, stack=stack, K_W=K_W)


def test_kw_scaling_linear():
    """
    K_W を2倍 → 中央変位 uz も2倍
    """
    V_rms = 10.0
    f_hz = 48_000.0

    rom1 = make_test_rom(K_W=1.0)
    rom2 = make_test_rom(K_W=2.0)

    uz1, I1 = rom1.frf_center_uz_and_I(V_rms, f_hz)
    uz2, I2 = rom2.frf_center_uz_and_I(V_rms, f_hz)

    # --- K_W scaling ---
    assert math.isclose(uz2 / uz1, 2.0, rel_tol=1e-2)

    # --- electrical should be unchanged ---
    assert math.isclose(I1, I2, rel_tol=1e-6)
