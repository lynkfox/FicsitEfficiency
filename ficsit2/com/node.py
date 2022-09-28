from __future__ import annotations
from dataclasses import dataclass, field, asdict
from ficsit2.com import machines, recipe, names, lookup
from typing import List, Optional
from copy import copy

DECIMAL_FORMAT = "{:.5g}"


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
            "product": [names.ComponentName(x) for x in self.products],
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
    product: names.ComponentName
    produces_per_cycle: float
    cycles_per_minute: float = field(init=False)
    production_chain_needs: recipe.ProductionChainStep = field(init=False)

    # Node Values
    node_depth: int = field(default=0)
    node_parent: Optional[ComponentNode] = field(default=None)
    node_children: List[ComponentNode] = field(init=False, default_factory=list)
    node_path_to_root: List[any] = field(init=False, default_factory=list)
    node_is_leaf: bool = field(init=False, default=False)

    def __post_init__(self):
        """
        Automatically converts recipe.Components per cycle to Child Component Nodes
        """
        self.cycles_per_minute = 60 / self.cycle_time
        self.needed_to_meet_parent_quota = (
            self.node_parent.parent_recipe_needs / self.produces_per_cycle
        )
        self.node_path_to_root = copy(self.node_parent.node_path_to_root)
        self.node_path_to_root.append(self)

        for component in self.components_per_cycle:
            child_component = ComponentNode(
                name=component.name,
                parent_recipe_needs=component.amount * self.needed_to_meet_parent_quota,
                node_parent=self,
                parent_cycles_per_minute=self.cycles_per_minute,
            )
            self._update_component_child(component, child_component)
            self.node_children.append(child_component)

        self._update_production_chain_step_values()

    def _update_production_chain_step_values(self):
        """
        Adds the pieces necessary for this current step in a given production chain
        """

        self.production_chain_needs = recipe.ProductionChainStep(
            recipe_name=self.name,
            components_produced=self.product,
            required_components=[
                recipe.Component(
                    name=component.name,
                    amount=component.amount * self.needed_to_meet_parent_quota,
                    is_per_minute=True,
                )
                for component in self.components_per_cycle
            ],
            machine_cost=recipe.RecipeMachineCost(
                machine=self.produced_in,
                total_machines=self.needed_to_meet_parent_quota
                / (self.produces_per_cycle * self.cycles_per_minute),
            ),
        )

    def _update_component_child(
        self, component: recipe.Component, child_component: ComponentNode
    ):
        """
        Updates the new child ComponentNode object with all necessary data that is auto populated or calculated from the path to root.
        """
        child_component.parent_recipe_needs_per_minute = (
            component.amount * self.cycles_per_minute
        )
        child_component.node_depth = self.node_depth + 1
        child_component.node_path_to_root = copy(self.node_path_to_root)
        child_component.node_path_to_root.append(child_component)

    def __str__(self) -> str:
        depth_indent = " ".join(["" for i in range((self.node_depth * 4))])
        number_to_produce = self.node_parent.parent_recipe_needs
        return (
            f"\n{depth_indent} ### {self.name}:\n"
            + f"{depth_indent}   : Needs\n"
            + " +\n".join(
                [
                    f"{depth_indent}   - {DECIMAL_FORMAT.format(ingredient.amount)} {ingredient.measurement}"
                    for ingredient in self.production_chain_needs.required_components
                ]
            )
            + f"\n{depth_indent}   > Produces > "
            + f"\n{depth_indent}              > ".join(
                [
                    f"{DECIMAL_FORMAT.format(number_to_produce)} {product.value} per minute"
                    for product in self.product
                ]
            )
            + "\n"
            + "\n".join([f"{component}" for component in self.node_children])
        )

    def as_dict(self):
        """
        outputs this node and its various pieces as a dictionary
        """
        raise NotImplementedError()


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
    parent_recipe_needs: float
    parent_cycles_per_minute: float = field(default=1)
    parent_recipe_needs_per_minute: float = field(default=0.0)

    node_parent: RecipeNode = field(default=None)
    node_path_to_root: List[any] = field(init=False, default_factory=list)
    node_children: List[RecipeNode] = field(init=False, default_factory=list)
    node_is_leaf: bool = field(init=False, default=False)
    node_depth: int = field(init=False, default=0)
    linked_component: recipe.Component = field(init=False, default=None)

    def __post_init__(self):
        self.node_is_leaf = self.name in lookup.ENDPOINTS

    def add_children(self, recipes: List[recipe.Recipe]) -> List[RecipeNode]:
        """
        Adds Alternative recipes for the component.

        Returns a list of all the recipe nodes to be added to the graph
        """

        for recipe in recipes:
            child_recipe = RecipeNode(
                **RecipeJson(**recipe).props(),
                node_parent=self,
                node_depth=self.node_depth + 1,
            )
            self.node_children.append(child_recipe)

        return self.node_children

    def as_dict(self):
        """
        outputs this node and its various pieces as a dictionary
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        depth_indent = " ".join(["" for i in range((self.node_depth * 4) + 5)])
        return (
            f"{depth_indent}|- Needs: {self.name.value} ({DECIMAL_FORMAT.format(self.parent_recipe_needs)}/min)"
            + "\n".join([str(recipe) for recipe in self.node_children])
        )
