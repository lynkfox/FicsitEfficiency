from com.constants import DataNames
from typing import List
import random

class Node():
    def init(self, node_name: str, data: dict):
        self.NODE_NAME = data[node_name]
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

    def add_parent(self, parent: Node):
        self.parent_node = parent

    def add_child(self, child: Node):
        self.children.append(child)

