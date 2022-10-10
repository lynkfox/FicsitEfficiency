from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import json
from ficsit2.com.machines import Machine
from ficsit2.com.names import ComponentName as ComponentName
from ficsit2.com import lookup
import math
from typing import Optional


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
class TotalProductionValues:
    power: int = field(default=0)
    machines: List[RecipeMachineCost] = field(default_factory=list)
    components: List[Component] = field(default_factory=list)
    longest_chain: int = field(default=0)
    total_area: float = field(default=0.0)

    def add_chain_step(self, production: ProductionChainStep):
        self.power += production.machine_cost.power
        self._add_machine(production.machine_cost)

        self.total_area += production.machine_cost.footprint

        for req_comp in production.required_components:
            self._add_component(req_comp)

        self.longest_chain = (
            production.current_step
            if production.current_step > self.longest_chain
            else self.longest_chain
        )

    def _add_component(self, other):
        """Combines like components, otherwise adding a new one to the list"""
        added_other_component = False
        for entry in self.components:
            if entry.name == other.name:
                entry.amount += other.amount
                added_other_component = True
                break

        if not added_other_component:
            self.components.append(other)

    def _add_machine(self, other):
        """Combines like machines, otherwise adding a new one to the list"""
        added_machine_values = False
        for entry in self.machines:
            if entry.machine.name == other.machine.name:
                entry.total_machines = math.ceil(entry.total_machines) + math.ceil(
                    other.total_machines
                )
                added_machine_values = True
                break

        if not added_machine_values:
            self.machines.append(other)

    def __str__(self):
        self.machines.sort(key=lambda x: x.machine.tierRequired)
        self.components.sort(key=lambda x: x.name.value)

        return (
            f"\t\033[93mTotal Power\033[0m: {self.power}\n"
            + f"\t\033[91mMachines:\033[0m\n"
            + f"\n".join(
                [
                    f"\t  - {machine.machine.name.value}: {math.ceil(machine.total_machines)}"
                    for machine in self.machines
                ]
            )
            + f"\n\t\033[96mComponents\033[0m:\n"
            + f"\n".join(
                [
                    f"\t  - {component.name.value}: {lookup.DECIMAL_FORMAT.format(component.amount)}{' m^3/min' if component.is_fluid else '/min'}"
                    for component in self.components
                    if component.name in lookup.ENDPOINTS
                ]
            )
            + f"\n\t\033[94mTotal Area\033[0m (give or take): {self.total_area} m^2\n"
            + f"\t  (or about {math.ceil(self.total_area/64)+len(self.machines)-1} foundations.)\n"
            + f"\t\033[1mLongest Product Chain\033[0m: {self.longest_chain/2}\n"
        )

    def __add__(self, other: TotalProductionValues):
        new_value = TotalProductionValues(
            power=self.power + other.power,
            machines=self.machines,
            components=self.components,
            longest_chain=self.longest_chain
            if self.longest_chain >= other.longest_chain
            else other.longest_chain,
            total_area=self.total_area + other.total_area,
        )

        for other_component in other.components:
            new_value._add_component(other_component)

        for other_machine in other.machines:
            new_value._add_machine(other_machine)

        return new_value


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


def load_recipes():
    with open("./ficsit2/data/recipes.json") as file:
        return json.load(file)
