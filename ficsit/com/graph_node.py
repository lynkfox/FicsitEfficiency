from ficsit.com.constants import DataNames
from typing import Dict, List, Union
import random


class Node:
    def __init__(self, node_name: str, data: dict) -> None:
        self.NODE_NAME = node_name
        self.ID = f"{self.NODE_NAME}{str(random.random())[2:5]}"

        self.display_name = data[DataNames.DISPLAY_NAME]
        self.machine_used = data[DataNames.PRODUCED_IN]
        self.number_produced = data[DataNames.PRODUCED_PER_CYCLE]
        self.components = data[DataNames.COMPONENTS]
        self.cycle_time = data[DataNames.TIME_TO_PRODUCE]
        self.manual_time_modifier = data[DataNames.MANUAL_CRAFT_MODIFIER]
        self.components_per_one = data[DataNames.COMPONENTS_PER_ONE]
        self.parent: Node = None
        self.children: List[Node] = []
        self.depth: int = 1

    def add_parent(self, parent):
        self.parent_node = parent

    def add_child(self, child):
        self.children.append(child)


class Graph:
    def __init__(self) -> None:
        self.Nodes: Dict[Node] = {}
        self.Root: Node = None
        self.depth: int = 0

    def add_root(self, root: Node) -> None:
        self.Root = root
        self.Nodes[root.ID] = root

    def add_child(self, parent: Union[Node, str], child: Node) -> Node:
        if isinstance(parent, str):
            id = parent
        else:
            id = parent.ID

        parent_in_graph = self.Nodes.get(id)
        if parent_in_graph is not None:
            parent_in_graph.add_child(child)
            child.add_parent(parent_in_graph)

            child.depth = parent_in_graph.depth + 1

            if child.depth > self.depth:
                self.depth = child.depth
