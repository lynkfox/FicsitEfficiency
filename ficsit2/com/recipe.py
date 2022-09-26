from __future__ import annotations
from dataclasses import dataclass
from typing import List
import json
from ficsit2.com.machines import Machine
from ficsit2.com.names import Component as ComponentName

@dataclass
class Component():
    name: ComponentName
    amount:float
    is_fluid: bool
    is_per_minute: bool

    def __post_init__(self):
        if self.is_fluid:
            self.amount = self.amount/100

    def as_dict(self):
        amount_key = "m^3/" if self.is_fluid else "items/"
        amount_time = "min" if self.is_per_minute else "productionCycle"
        return { 
            "name": self.name.name, 
            "amount": self.amount, 
            "measurement":  amount_key+amount_time,
            "isFluid": self.is_fluid
            }

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)

    def __add__(self, other: Component):
        if not isinstance(other, Component):
            raise TypeError("Components can only be added to Components")

        if self.name != other.name:
            raise ValueError(f"{self.name} cannot be added to {other.name}")

        return Component(name=self.name, amount=self.amount+other.amount , is_fluid=self.is_fluid)

    def __eq__(self, other:Component):
        if not isinstance(other, Component):
            raise TypeError("Components can compared to other Components")

        return self.name == other.name


@dataclass
class ComponentsUsed():
    recipes_used: List[str]
    steps:int
    components: List[Component]


@dataclass
class ProductionChain():
    paths: List(ComponentsUsed)

@dataclass
class Recipe():
    name: str
    product: str
    produced_in: Machine
    produced_per_cycle: float
    cycle_time: float
    components_per_cycle: List[Component]
    produced_per_minute: float
    components_per_minute: List[Component]

