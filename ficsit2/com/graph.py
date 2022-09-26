from ficsit2.com import node
from dataclasses import dataclass, field
from typing import List, Set, Union


@dataclass
class Graph:
    """
    A tree of nodes, each node representing a Recipe or Component
    """

    root: node.ComponentNode
    total_depth: int = field(init=False, default=0)
    recipe_nodes: List[node.RecipeNode] = field(init=False, default_factory=[])
    component_nodes: Set[node.ComponentNode] = field(init=False, default_factory=[])
    paths_to_root: List[list] = field(init=False, default_factory=[])
    leafs = List[any] = field(init=False, default_factory=[])
