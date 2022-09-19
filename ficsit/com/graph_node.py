from __future__ import annotations
from ficsit.com.constants import DataNames
from typing import Dict, List, Union, Optional
from uuid import uuid4
from dataclasses import dataclass
from ficsit.com.machines import iMachine, Miner

@dataclass
class NodeProps():
    recipeName: str
    producedIn: Union[str,iMachine]
    producesPerCycle: int
    components: Optional[dict]
    componentsPerMinute: Optional[dict]
    cycleTime: int
    manualMultiplier: int

    def as_dict(self):
        return {
            DataNames.DISPLAY_NAME: self.recipeName,
            DataNames.PRODUCED_IN: self.producedIn,
            DataNames.PRODUCED_PER_CYCLE: self.producesPerCycle,
            DataNames.COMPONENTS: self.components,
            DataNames.TIME_TO_PRODUCE: self.componentsPerMinute,
            DataNames.MANUAL_CRAFT_MODIFIER: self.cycleTime,
            DataNames.COMPONENTS_PER_ONE: self.manualMultiplier
        }




class Node:
    def __init__(self, node_name: str, data: Union[dict, NodeProps]) -> None:
        self.NODE_NAME = node_name
        self.ID = f"{self.NODE_NAME[:4]}-ID-{str(uuid4()).replace('-', '')}"
        
        if isinstance(data, NodeProps):
            data = data.as_dict()

        self.display_name = data[DataNames.DISPLAY_NAME]
        self.machine_used = data[DataNames.PRODUCED_IN]
        self.number_produced = data[DataNames.PRODUCED_PER_CYCLE]
        self.components = data[DataNames.COMPONENTS]
        self.cycle_time = data[DataNames.TIME_TO_PRODUCE]
        self.cycles_per_minute = 60/self.cycle_time if self.cycle_time is not None and self.cycle_time > 0 else 0
        self.manual_time_modifier = data[DataNames.MANUAL_CRAFT_MODIFIER]
        self.components_per_one = data[DataNames.COMPONENTS_PER_ONE]
        self.parent: Node = None
        self.parent_child_edge_name: str = None
        self.needed_for_one_parent: int = 0
        self.needed_for_parent_cycle: int = 0
        self.children: List[Node] = []
        self.path_to_root: List[Node] = []
        self.depth: int = 0

    def add_child(self, child: Node, parent_child_path_name:str):
        """
        Adds a child to this node and increments the depth of the child by 1.
        """
        self.children.append(child)
        child.parent_child_edge_name = parent_child_path_name
        child.parent = self
        child.depth = self.depth+1
        child.needed_for_parent_cycle = self.components.get(child.NODE_NAME, 0)
        # parent_asks_for = self.components_per_one.get(child.NODE_NAME, 0) if self.components_per_one is not None else 0
        # child.needed_for_one_parent = self.parent.needed_for_one_parent if self.needed_for_one_parent != 0 else parent_asks_for
        child.path_to_root = [*self.path_to_root, *[self]]

    def add_parent(self, parent: Node):
        """
        Adds the parent node of this node.
        """
        self.parent_node = parent

    def as_dict(self):
        return { key:self._Node_list_serialize(value) for key, value in self.__dict__.items() if not key.startswith("__")}

    def _Node_list_serialize(self, value):
        """
        for handling the List[Node] in as_dict
        """
        if isinstance(value, Node):
            return value.NODE_NAME

        if value is Miner:
            return value.display_name

        if not isinstance(value, List) or (isinstance(value, List) and (len(value) == 0 or not isinstance(value[0], Node))):
            print(value)
            return value

        return [node.NODE_NAME for node in value]


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

    def attach_child(self, parent: Node, child: Optional[Node], edge_name: Optional[str]=None) -> Node:
        """
        Adds a child to a parent node. Increments max_depth if necessary,
        if child is None adds the parent to the endpoints list.
        """
        if parent is None:
            return
        parent.add_child(child, edge_name)
        self.Nodes[child.ID] = child
        self.max_depth = child.depth if child.depth > self.max_depth else self.max_depth

        return child
            

    def define_endpoint(self, end_node: Node):
        """
        Attaches one final child to the path, treating it as an endpoint
        """
        self.endpoints.append(end_node)
        end_node.path_to_root.append(end_node)
        self.all_paths_to_root.append(end_node.path_to_root)

    def calculate_weights(self):
        pass


    def json_output(self, node: Optional[Node] = None) -> dict:
        """
        Outputs the Graph as a json of objects of objects.
        """

        if node is None:
            node = self.Root
        
        parent = node.as_dict()
        parent["children"] = [self.json_output(node=child) for child in node.children()]
        return parent

             
            
            
    