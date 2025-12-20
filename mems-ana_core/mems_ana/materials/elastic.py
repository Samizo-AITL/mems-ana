from dataclasses import dataclass


@dataclass(frozen=True)
class IsoElastic:
    E: float
    nu: float
    rho: float


IsotropicElastic = IsoElastic
