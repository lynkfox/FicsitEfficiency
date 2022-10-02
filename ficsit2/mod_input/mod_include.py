from typing import List, Tuple
from ficsit2.com.machines import Machine
from enum import Enum
import json


class ModdedContent:
    def __init__(self) -> None:
        modded_items = load_modded_items()
        self.component = generate_modded_component_enum(modded_items["items"])
        self.buildable, self.machine_map = generate_modded_machines(
            modded_items["machines"]
        )


def load_modded_items():
    with open("./ficsit2/data/modded_items.json") as json_file:
        modded_items = json.load(json_file)

    return modded_items


def generate_modded_component_enum(items: List[str]) -> Enum:
    """
    reads the ficsit2/data/modded_items.json (generated through the -m flag on build_recipes.py)
    and generate an enum for use at run time of the graph efficiency
    """
    enum_input = {enum_name(name): name for name in items}

    return Enum("ModdedComponent", enum_input)


def generate_modded_machines(machines: List[str]) -> Tuple[Enum, dict]:
    """
    reads the ficsit2/data/modded_items.json (generated through the -m flag on build_recipes.py)
    and generate an enum and mapping for each
    """
    enum_input = {enum_name(name): name for name in machines}
    ModdedBuildable = Enum("ModdedBuildable", enum_input)

    mapping = {
        ModdedBuildable(machine): Machine(
            name=ModdedBuildable(machine),
            tierRequired=0,
            powerUse=0,
            footprint=1,
            width=1,
            length=1,
            height=1,
        )
        for machine in machines
    }

    return ModdedBuildable, mapping


def enum_name(str):
    return str.replace(":", "").replace(" ", "_").upper()
