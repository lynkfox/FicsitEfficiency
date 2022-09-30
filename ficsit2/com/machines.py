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


machine_map = {
    Buildable.MINER: Machine(
        name=Buildable.MINER,
        tierRequired=(0.5, 4.1, 8.3),
        powerUse=(5, 12, 30),
        width=6,
        length=14,
        height=18,
        footprint=84,
    ),
    Buildable.SMELTER: Machine(
        name=Buildable.SMELTER,
        tierRequired=0.2,
        powerUse=4,
        width=6,
        length=9,
        height=9,
        footprint=54,
    ),
    Buildable.FOUNDRY: Machine(
        name=Buildable.FOUNDRY,
        tierRequired=3.3,
        powerUse=16,
        width=10,
        length=9,
        height=9,
        footprint=90,
    ),
    Buildable.CONSTRUCTOR: Machine(
        name=Buildable.CONSTRUCTOR,
        powerUse=4,
        footprint=80,
        tierRequired=0.3,
        width=8,
        length=10,
        height=8,
    ),
    Buildable.ASSEMBLER: Machine(
        name=Buildable.ASSEMBLER,
        tierRequired=2.1,
        powerUse=15,
        width=10,
        length=15,
        height=11,
        footprint=150,
    ),
    Buildable.MANUFACTURER: Machine(
        name=Buildable.MANUFACTURER,
        tierRequired=5.2,
        powerUse=55,
        width=18,
        length=19,
        height=12,
        footprint=342,
    ),
    Buildable.REFINERY: Machine(
        name=Buildable.REFINERY,
        tierRequired=5.1,
        powerUse=30,
        width=10,
        length=20,
        height=31,
        footprint=200,
    ),
    Buildable.PACKAGER: Machine(
        name=Buildable.PACKAGER,
        tierRequired=5.3,
        powerUse=10,
        width=8,
        length=8,
        height=12,
        footprint=64,
    ),
    Buildable.BLENDER: Machine(
        name=Buildable.BLENDER,
        tierRequired=7.1,
        powerUse=75,
        width=18,
        length=19,
        height=12,
        footprint=342,
    ),
    Buildable.PARTICLE_ACCELERATOR: Machine(
        name=Buildable.PARTICLE_ACCELERATOR,
        tierRequired=8.4,
        powerUse=1500,
        width=24,
        length=38,
        height=32,
        footprint=912,
    ),
    Buildable.NUCLEAR_POWER_PLANT: Machine(
        name=Buildable.NUCLEAR_POWER_PLANT,
        tierRequired=8.1,
        powerUse=-2500,
        width=38,
        length=43,
        height=49,
        footprint=1634,
    ),
}
