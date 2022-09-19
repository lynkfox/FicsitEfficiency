from __future__ import annotations
from ficsit.com.constants import DataNames
from typing import Dict, List, Union, Optional
from uuid import uuid4
from dataclasses import dataclass
from ficsit.com.machines import iMachine, Miner
from copy import deepcopy


@dataclass
class NodeProps:
    recipeName: str
    producedIn: Union[str, iMachine]
    producesPerCycle: int
    components: Optional[dict]
    componentsPerMinute: Optional[dict]
    cycleTime: int
    cyclesPerMinute: float
    manualMultiplier: int

    def as_dict(self):
        return {
            DataNames.DISPLAY_NAME: self.recipeName,
            DataNames.PRODUCED_IN: self.producedIn,
            DataNames.PRODUCED_PER_CYCLE: self.producesPerCycle,
            DataNames.COMPONENTS_PER_CYCLE: self.components,
            DataNames.CYCLE_TIME: self.componentsPerMinute,
            DataNames.MANUAL_CRAFT_MODIFIER: self.cycleTime,
            DataNames.CYCLES_PER_MINUTE: self.cyclesPerMinute,
            DataNames.COMPONENTS_PER_MINUTE: self.manualMultiplier,
        }


class Node:
    def __init__(self, node_name: str, data: Union[dict, NodeProps]) -> None:
        self.NODE_NAME = node_name
        self.ID = f"{self.NODE_NAME[:4]}-ID-{str(uuid4()).replace('-', '')}"

        if isinstance(data, NodeProps):
            data = data.as_dict()

        self.display_name: str = data[DataNames.DISPLAY_NAME]
        self.produced_in: Union[str, iMachine] = data[DataNames.PRODUCED_IN]
        self.cycle_time: float = data[DataNames.CYCLE_TIME]
        self.produced_per_cycle: int = data[DataNames.PRODUCED_PER_CYCLE]
        self.components_per_cycle: Dict[str, Union[float, int]] = data[
            DataNames.COMPONENTS_PER_CYCLE
        ]
        self.cycles_per_minute: float = data[DataNames.CYCLES_PER_MINUTE]
        self.components_per_minute: Dict[str, float] = data[
            DataNames.COMPONENTS_PER_MINUTE
        ]
        self.depth: int = 0
        self.children: List[Node] = []
        self.path_to_root: List[Node] = []
        self.parent: Node = None
        self.parent_child_edge_name: str = None
        self.needed_for_parent_per_minute: int = 0
        self.needed_for_parent_cycle: int = 0

        self.base_components_per_minute_totals: List[Dict[str, float]] = []

    def add_child(self, child: Node, parent_child_path_name: str):
        """
        Adds a child to this node and increments the depth of the child by 1.
        """
        self.children.append(child)
        child.parent_child_edge_name = parent_child_path_name
        child.parent = self
        child.depth = self.depth + 1
        child.needed_for_parent_cycle = self.components_per_cycle.get(
            child.NODE_NAME, 0
        )
        child.needed_for_parent_per_minute = self.components_per_minute.get(
            child.NODE_NAME, 0
        )
        # parent_asks_for = self.components_per_one.get(child.NODE_NAME, 0) if self.components_per_one is not None else 0
        # child.needed_for_one_parent = self.parent.needed_for_one_parent if self.needed_for_one_parent != 0 else parent_asks_for
        child.path_to_root = [*self.path_to_root, *[self]]

    def add_parent(self, parent: Node):
        """
        Adds the parent node of this node.
        """
        self.parent_node = parent

    def as_dict(self):
        return {
            key: self._Node_list_serialize(value)
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        }

    def _Node_list_serialize(self, value):
        """
        for handling the List[Node] in as_dict
        """
        if isinstance(value, Node):
            return value.NODE_NAME

        if value is Miner:
            return value.display_name

        if not isinstance(value, List) or (
            isinstance(value, List)
            and (len(value) == 0 or not isinstance(value[0], Node))
        ):
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

    def attach_child(
        self, parent: Node, child: Optional[Node], edge_name: Optional[str] = None
    ) -> Node:
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
        self._update_parent_base_materials(end_node)

    def _update_parent_base_materials(self, current: Node, uplift: dict = None):
        """
        Traverses back up the tree from an leaf, updating each parent with new totals for the given paths below
        """

        next_uplift = (
            deepcopy(current.parent.components_per_minute)
            if uplift is None
            else deepcopy(uplift)
        )

        if current.parent is not None:

            for component, amount in next_uplift.items():
                if component == "Path":
                    next_uplift[
                        "Path"
                    ] = f"{current.parent.display_name}->{next_uplift['Path']}"
                    continue

                if current.parent.needed_for_parent_cycle > 0:
                    next_uplift[component] = (
                        amount * current.parent.needed_for_parent_cycle
                    )

            if "Path" not in next_uplift.keys():
                next_uplift["Path"] = current.parent.display_name

            seen = set()
            reduced_paths = []
            for component_set in current.parent.base_components_per_minute_totals:
                if component_set["Path"] not in seen:
                    seen.add(component_set["Path"])
                    reduced_paths.append(component_set)

            if next_uplift["Path"] not in seen:
                reduced_paths.append(next_uplift)

            current.parent.base_components_per_minute_totals = reduced_paths

            self._update_parent_base_materials(current.parent, next_uplift)

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
