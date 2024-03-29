from __future__ import annotations
from dataclasses import dataclass, field
from ficsit2.com import machines, recipe, names, lookup
from typing import List, Optional
from copy import copy
from ficsit2.com import lookup
from ficsit2.mod_input.mod_include import ModdedContent


from ficsit2.com.lookup import DECIMAL_FORMAT


def _try_for_modded_component(mod_content, name):
    """
    tries various names to see which fits
    """
    if mod_content is not None:
        try:
            return names.ComponentName(name)
        except Exception:
            return mod_content.component(name)
    else:  # let it error if no mod content
        return names.ComponentName(name)


def _try_for_modded_buildable(mod_content, name):

    if mod_content is not None:
        try:
            return names.Buildable(name)
        except Exception:
            return mod_content.buildable(name)
    else:  # let it error if no mod content
        return names.Buildable(name)


@dataclass
class RecipeJson:
    """
    Converts the JSON file format (camel case) dictionary loaded from the recipes.json for a single recipe
    into the necessary fields for the Recipe Node
    """

    recipeName: str
    products: list  # all products produced by this recipe
    product: names.ComponentName  # product we actually want
    producedIn: str
    producesPerCycle: float
    cycleTime: float
    components: list
    mod_content: ModdedContent

    def props(self):
        building = _try_for_modded_buildable(self.mod_content, self.producedIn)
        return {
            "name": self.recipeName,
            "all_products": [
                _try_for_modded_component(self.mod_content, x) for x in self.products
            ],
            "product": self.product,
            "produced_in": lookup.machine_map.get(
                building, self.mod_content.machine_map.get(building)
            ),
            "cycle_time": self.cycleTime,
            "produces_per_cycle": self.producesPerCycle,
            "components_per_cycle": [
                recipe.Component(
                    name=_try_for_modded_component(self.mod_content, x["name"]),
                    amount=x["amount"],
                )
                for x in self.components
            ],
            "mod_content": self.mod_content,
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
    all_products: List[names.ComponentName]
    produces_per_cycle: float
    cycles_per_minute: float = field(init=False)
    production_chain_costs: recipe.ProductionChainStep = field(init=False)

    # Node Values
    node_depth: int = field(default=0)
    node_parent: Optional[ComponentNode] = field(default=None)
    node_children: List[ComponentNode] = field(init=False, default_factory=list)
    node_path_to_root: List[any] = field(init=False, default_factory=list)
    node_is_leaf: bool = field(init=False, default=False)
    mod_content: ModdedContent = field(default=False)

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
                mod_content=self.mod_content,
            )
            self._update_component_child(component, child_component)
            self.node_children.append(child_component)

        self._update_production_chain_step_values()

    def _update_production_chain_step_values(self):
        """
        Adds the pieces necessary for this current step in a given production chain
        """

        self.production_chain_costs = recipe.ProductionChainStep(
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
            current_step=self.node_depth + 1,
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
        depth_indent = " ".join(["" for i in range((self.node_depth * 3))])
        number_to_produce = self.node_parent.parent_recipe_needs

        return (
            f"\n{depth_indent}# {self.name}:"
            + f"\n{depth_indent}  | Input/Output and Step Efficiency Values:"
            + str(self.production_chain_costs).replace("\n", f"\n{depth_indent}")
            + (
                f"\n{depth_indent}      ++ {DECIMAL_FORMAT.format(number_to_produce)} {self.product.value} per minute"
                if self.product is not None
                else ""
            )
            + "".join([f"{component}" for component in self.node_children])
            if len(self.node_children) > 0
            else ""
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
    mod_content: ModdedContent = field(default=None)

    def __post_init__(self):
        self.node_is_leaf = self.name in lookup.ENDPOINTS

    def add_children(
        self, parent: Optional[RecipeNode], recipes: List[recipe.Recipe]
    ) -> List[RecipeNode]:
        """
        Adds Alternative recipes for the component.

        Returns a list of all the recipe nodes to be added to the graph
        """

        for recipe in recipes:
            recipe_name = (
                recipe.get("recipeName")
                if isinstance(recipe, dict)
                else recipe.name.value
            )
            if self._potential_infinite_loop(recipe_name):
                # print(f"{recipe_name} was already found in path to root, skipping potential infinite loop")
                continue
            child_recipe = RecipeNode(
                **RecipeJson(
                    **{
                        **recipe,
                        **{"mod_content": self.mod_content, "product": self.name},
                    }
                ).props(),
                node_parent=self,
                node_depth=self.node_depth + 1,
            )
            self.node_children.append(child_recipe)

        if parent is not None:
            self.node_path_to_root = parent.node_path_to_root

        self.node_path_to_root.append(self)

        return self.node_children

    def as_dict(self):
        """
        outputs this node and its various pieces as a dictionary
        """
        raise NotImplementedError()

    def _potential_infinite_loop(self, recipe_name: str):
        """
        Functionality to prevent potential infinite loops (usually between Rubber and Plastic with the Recycled Variant loops)
        """

        return recipe_name in [
            previous_recipe.name
            for previous_recipe in self.node_path_to_root
            if isinstance(previous_recipe, RecipeNode)
        ]

    def __str__(self) -> str:
        depth_indent = " ".join(["" for i in range((self.node_depth * 3) - 1)])
        return (
            f"\n{depth_indent}|- {self.name.value} ({DECIMAL_FORMAT.format(self.parent_recipe_needs)}/min)"
            + "".join([str(recipe) for recipe in self.node_children])
            if len(self.node_children) > 0
            else ""
        )
