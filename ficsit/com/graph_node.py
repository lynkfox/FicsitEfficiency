from __future__ import annotations
from ficsit.com.constants import DataNames
from typing import Dict, List, Union, Optional
from uuid import uuid4

class Node:
    def __init__(self, node_name: str, data: dict) -> None:
        self.NODE_NAME = node_name
        self.ID = f"{self.NODE_NAME[:4]}-ID-{str(uuid4()).replace('-', '')}"

        self.display_name = data[DataNames.DISPLAY_NAME]
        self.machine_used = data[DataNames.PRODUCED_IN]
        self.number_produced = data[DataNames.PRODUCED_PER_CYCLE]
        self.components = data[DataNames.COMPONENTS]
        self.cycle_time = data[DataNames.TIME_TO_PRODUCE]
        self.manual_time_modifier = data[DataNames.MANUAL_CRAFT_MODIFIER]
        self.components_per_one = data[DataNames.COMPONENTS_PER_ONE]
        self.parent: Node = None
        self.parent_component: str = None
        self.children: List[Node] = []
        self.path_to_root: List[Node] = []
        self.depth: int = 0

    def add_child(self, child: Node, child_identifier:str):
        """
        Adds a child to this node and increments the depth of the child by 1.
        """
        self.children.append(child)
        child.parent_component = child_identifier
        child.parent = self
        child.depth = self.depth+1
        child.path_to_root = [*self.path_to_root, *[self]]

    def add_parent(self, parent: Node):
        """
        Adds the parent node of this node.
        """
        self.parent_node = parent

    def as_dict(self):
        return { key:value for key, value in self.__dict__ if not key.startswith("__")}


class Graph:
    def __init__(self) -> None:
        self.Nodes: Dict[Node] = {}
        self.Root: Node = None
        self.max_depth: int = 0
        self.endpoints: List[Node] = []
        self.all_paths_to_root = []

    def add_root(self, root: Node) -> None:
        self.Root = root
        self.Nodes[root.ID] = root

    def attach_child(self, parent: Node, child: Optional[Node], child_identifier: Optional[str]=None):
        """
        Adds a child to a parent node. Increments max_depth if necessary,
        if child is None adds the parent to the endpoints list.
        """
        if parent is None:
            return
        parent.add_child(child, child_identifier)
        self.Nodes[child.ID] = child
        self.max_depth = child.depth if child.depth > self.max_depth else self.max_depth

        return child
            

    def update_endpoints(self, end_node: Node):
        """
        Adds the path of nodes from an endpoint
        """
        self.endpoints.append(end_node)
        self.all_paths_to_root.append([*end_node.path_to_root, *[end_node]])


    def json_output(self, node: Optional[Node] = None) -> dict:
        """
        Outputs the Graph as a json of objects of objects.
        """

        if node is None:
            node = self.Root
        
        parent = node.as_dict()
        parent["children"] = [self.json_output(node=child) for child in node.children()]
        return parent

             
            
            
    