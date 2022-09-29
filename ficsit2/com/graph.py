from ficsit2.com import node
from dataclasses import dataclass, field
from typing import List, Set, Union, Any
import functools
import operator


@dataclass
class Graph:
    """
    A tree of nodes, each node representing a Recipe or Component
    """

    root: node.ComponentNode
    recipe_tree: dict
    total_depth: int = field(init=False, default=0)
    paths_to_root: List[list] = field(init=False, default_factory=list)
    leafs: List[Any] = field(init=False, default_factory=list)

    def __post_init__(self):

        self.json_add_children(self.root, self.recipe_tree[self.root.name.value])
        for recipe_child in self.root.node_children:
            self.add_children_recipes_for(recipe_child.node_children)

    def json_add_children(self, parent: node.ComponentNode, children: List[dict]):
        """
        Adds children recipes to the given component node, based on the json input
        """

        if isinstance(parent, node.RecipeNode):
            raise TypeError("json_add_children must start with a ComponentNode")

        parent.add_children(recipes=children)

        self.total_depth = (
            parent.node_depth + 1 if not parent.node_is_leaf else parent.node_depth
        )

    def add_children_recipes_for(self, recipe_components: list):
        component: node.ComponentNode
        for component in recipe_components:
            if not component.node_is_leaf:
                component_child_recipes = component.add_children(
                    self.recipe_tree[component.name.value]
                )
                self.add_children_recipes_for(
                    functools.reduce(
                        operator.iconcat,
                        [recipe.node_children for recipe in component_child_recipes],
                        [],
                    )
                )
            else:
                self.leafs.append(component)
                self.total_depth = (
                    component.node_depth
                    if component.node_depth > self.total_depth
                    else self.total_depth
                )
                self.paths_to_root.append(component.node_path_to_root)