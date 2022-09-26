from __future__ import annotations
from dataclasses import dataclass, field
from ficsit2.com import machines, recipe, names, lookup
from typing import List
from copy import copy

@dataclass
class RecipeNode():
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
    cycles_per_minute: float = field(init=False)

    # Node Values
    node_children: List[ComponentNode] = field(init=False)
    node_parent: ComponentNode = field(init=False)
    node_depth: int = field(init=False)
    node_path_to_root: List[any] = field(init=False)
    node_is_leaf: bool = field(init=False, default=False)


    def __post_init__(self):
        """
        Automatically converts recipe.Components per cycle to Child Component Nodes
        """
        self.cycles_per_minute = 60/self.cycle_time

        for component in self.components_per_cycle:
            child_component = ComponentNode(
                name=component.name,
                recipe_needs=component.amount
            )

            child_component.recipe_needs_per_minute = component.amount*self.cycles_per_minute
            child_component.node_parent = self
            child_component.node_depth = self.node_depth+1
            child_component.node_path_to_root = copy(self.node_path_to_root)
            child_component.node_path_to_root.append(child_component)

            if child_component.name in lookup.ENDPOINTS:
                child_component.node_is_leaf = True

            self.node_children = child_component
    
@dataclass
class ComponentNode():
    """
    Represents a Component Node on the graph of recipes
    
    Its parent will always be a RecipeNode
    Its children will always be Recipe Nodes
    Its siblings will always be other Component Nodes
    """
    name: names.Component

    # efficiency_values
    recipe_needs: float
    recipe_needs_per_minute: float = field(init=False)
    parent_needs_per_minute: float = field(init=False)
    
    node_path_to_root: List[any] = field(init=False)
    node_children: List[RecipeNode] = field(init=False)
    node_is_leaf: bool = field(init=False)
    node_depth: int = field(init=False)
    node_parent: RecipeNode = field(init=False)

    def add_children(self, recipes:List[recipe.Recipe]):
        """
        Adds Alternative recipes for the component
        """

        for recipe in recipes:
            child_recipe = RecipeNode(
                name=recipe.name,
                produced_in=recipe.produced_in,
                cycle_time=recipe.cycle_time,
                components_per_cycle=recipe.components_per_cycle
            )

            child_recipe.node_parent=self
            child_recipe.node_depth = self.node_depth+1
            child_recipe.node_path_to_root = copy(self.node_path_to_root)
            child_recipe.node_path_to_root.append(child_recipe)

