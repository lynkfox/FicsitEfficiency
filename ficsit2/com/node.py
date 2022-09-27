from __future__ import annotations
from dataclasses import dataclass, field
from ficsit2.com import machines, recipe, names, lookup
from typing import List, Optional
from copy import copy


@dataclass
class RecipeJson:
    """
    Converts the JSON file format (camel case) dictionary loaded from the recipes.json for a single recipe
    into the necessary fields for the Recipe Node
    """

    recipeName: str
    products: list
    producedIn: str
    producesPerCycle: float
    cycleTime: float
    components: list

    def props(self):
        return {
            "name": self.recipeName,
            "produces": [names.ComponentName(x) for x in self.products],
            "produced_in": machines.machine_map.get(names.Buildable(self.producedIn)),
            "cycle_time": self.cycleTime,
            "produces_per_cycle": self.producesPerCycle,
            "components_per_cycle": [
                recipe.Component(
                    name=names.ComponentName(x["name"]), amount=x["amount"]
                )
                for x in self.components
            ],
        }


@dataclass
class RecipeNode:
    """
    A Recipe Node

    This represents one potential alternate recipe on the graph, including its various parts.

    Its children should always be Component Nodes

    Its parent should always be a single Component Node
    """

    # Recipe values
    name: str
    produced_in: machines.Machine
    cycle_time: float
    components_per_cycle: List[recipe.Component]
    produces: names.ComponentName
    produces_per_cycle: float
    cycles_per_minute: float = field(init=False)

    # Node Values
    node_children: List[ComponentNode] = field(init=False, default_factory=list)
    node_parent: Optional[ComponentNode] = field(init=False, default=None)
    node_depth: int = field(init=False, default=0)
    node_path_to_root: List[any] = field(init=False, default_factory=list)
    node_is_leaf: bool = field(init=False, default=False)

    def __post_init__(self):
        """
        Automatically converts recipe.Components per cycle to Child Component Nodes
        """
        self.cycles_per_minute = 60 / self.cycle_time

        for component in self.components_per_cycle:
            child_component = ComponentNode(
                name=component.name, recipe_needs=component.amount
            )
            self._update_component_child(component, child_component)
            self.node_children.append(child_component)

    def _update_component_child(
        self, component: recipe.Component, child_component: ComponentNode
    ):
        """
        Updates the new child ComponentNode object with all necessary data that is auto populated or calculated from the path to root.
        """
        child_component.recipe_needs_per_minute = (
            component.amount * self.cycles_per_minute
        )
        child_component.node_parent = self
        child_component.node_depth = self.node_depth + 2
        child_component.node_path_to_root = copy(self.node_path_to_root)
        child_component.node_path_to_root.append(child_component)

    def __str__(self) -> str:
        depth_indent = " ".join(["" for i in range((self.node_depth * 4) + 1)])

        return (
            f"\n{depth_indent}### {self.name}:\n"
            + "\n".join(
                [
                    f"{depth_indent}  |- {ingredient.formatted()}"
                    for ingredient in self.components_per_cycle
                ]
            )
            + "\n"
            + "\n".join([f"{component}" for component in self.node_children])
        )


@dataclass
class ComponentNode:
    """
    Represents a Component Node on the graph of recipes

    Its parent will always be a RecipeNode
    Its children will always be Recipe Nodes
    Its siblings will always be other Component Nodes
    """

    name: names.ComponentName

    # efficiency_values
    recipe_needs: float
    recipe_needs_per_minute: float = field(init=False, default=0.0)
    parent_needs_per_minute: float = field(init=False, default=0.0)

    node_path_to_root: List[any] = field(init=False, default_factory=list)
    node_children: List[RecipeNode] = field(init=False, default_factory=list)
    node_is_leaf: bool = field(init=False, default=False)
    node_depth: int = field(init=False, default=0)
    node_parent: RecipeNode = field(init=False, default=None)
    linked_component: recipe.Component = field(init=False, default=None)

    def __post_init__(self):
        self.node_is_leaf = self.name in lookup.ENDPOINTS

    def add_children(self, recipes: List[recipe.Recipe]) -> List[RecipeNode]:
        """
        Adds Alternative recipes for the component.

        Returns a list of all the recipe nodes to be added to the graph
        """

        for recipe in recipes:
            child_recipe = RecipeNode(**RecipeJson(**recipe).props())
            self._update_recipe_child(child_recipe)
            self.node_children.append(child_recipe)

        return self.node_children

    def _update_recipe_child(self, child_recipe: RecipeNode):
        """
        Updates the new child RecipeNode with all necessary data that is auto populated or calculated from the path to root.
        """
        child_recipe.node_parent = self
        child_recipe.node_depth = self.node_depth + 1
        child_recipe.node_path_to_root = copy(self.node_path_to_root)
        child_recipe.node_path_to_root.append(child_recipe)

    def __str__(self) -> str:
        depth_indent = " ".join(["" for i in range((self.node_depth * 4) + 1)])
        return (
            f"{depth_indent} === {self.name.value} ( {self.parent_needs_per_minute} to satisfy parent)"
            + "\n".join([str(recipe) for recipe in self.node_children])
        )
