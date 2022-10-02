from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import json
from ficsit2.com.machines import Machine
from ficsit2.com.names import ComponentName as ComponentName
from ficsit2.com import lookup
import math


@dataclass
class Component:
    name: ComponentName
    amount: float
    is_fluid: bool = field(init=False, default=False)
    is_per_minute: bool = field(default=False)

    def __post_init__(self):
        self.is_fluid = self.name in lookup.FLUIDS
        self.measurement = (
            f'{self.name.value+" m^3" if self.is_fluid else self.name.value+"(s)"}'
        )
        self.rate = f'{"/min" if self.is_per_minute else "/cycle"}'

    def as_dict(self):

        return {
            "name": self.name.value,
            "amount": self.amount,
            "measurement": self.measurement + self.rate,
        }

    def formatted(self, cycles_per_minute: int = 1, offset: float = 1.0) -> str:
        """
        returns a formatted string output for use in the output of a larger graph

        :param cycles_per_minute - how many cycles this component will be used in
        :param offset - how much to offset the amount ( a fraction ) based on the above
        """

        return (
            f"{'{:.4f}'.format(self.amount*cycles_per_minute*offset)} {self.name.value}"
        )

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)

    def __add__(self, other: Component):
        if not isinstance(other, Component):
            raise TypeError("Components can only be added to Components")

        if self.name != other.name:
            raise ValueError(f"{self.name} cannot be added to {other.name}")

        return Component(name=self.name, amount=self.amount + other.amount)

    def __eq__(self, other: Component):
        if not isinstance(other, Component):
            raise TypeError("Components can compared to other Components")

        return self.name == other.name


@dataclass
class RecipeMachineCost:
    machine: Machine
    total_machines: float
    power: float = field(init=False, default=0.0)
    footprint: float = field(init=False, default=0.0)
    volume: float = field(init=False, default=0.0)

    def __post_init__(self):
        self.power = self.machine.powerUse * math.ceil(self.total_machines)
        self.footprint = (self.machine.length * self.machine.width) * math.ceil(
            self.total_machines
        )
        self.volume = self.footprint * self.machine.height


@dataclass
class ProductionChainStep:
    recipe_name: str
    components_produced: str
    required_components: List[Component]
    machine_cost: RecipeMachineCost
    current_step: int

    def __str__(self):

        return "".join(
            [
                "",
                " ".join(
                    [
                        f"\n      - {lookup.DECIMAL_FORMAT.format(ingredient.amount)} {ingredient.measurement}"
                        for ingredient in self.required_components
                    ]
                    if len(self.required_components) > 0
                    else ""
                ),
                f"\n      - {math.ceil(self.machine_cost.power)} MW(s)",
                f"\n      * {math.ceil(self.machine_cost.total_machines)} {self.machine_cost.machine.name.value}(s)",
                f"\n      * {math.ceil(self.machine_cost.footprint)} m^2(s) (about {math.ceil(self.machine_cost.footprint/64)} foundations minus belt space)",
                f"\n      * {self.current_step/2} steps into the chain from the top.",
            ]
        )


@dataclass
class Recipe:
    name: str
    product: str
    produced_in: Machine
    produced_per_cycle: float
    cycle_time: float
    components_per_cycle: List[Component]
    produced_per_minute: float
    components_per_minute: List[Component]
