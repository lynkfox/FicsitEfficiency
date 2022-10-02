from __future__ import annotations
from dataclasses import dataclass
from ficsit2.com.names import Buildable


@dataclass
class Machine:
    name: Buildable
    tierRequired: float
    powerUse: float  # in MW
    footprint: float  # in m^2
    width: float  # in meters
    length: float
    height: float
