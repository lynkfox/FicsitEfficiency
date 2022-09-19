from ficsit.com.utils import load_recipes, display_name
from ficsit.com import components as GameComponents
from ficsit.com.graph_node import Graph, Node, NodeProps
from typing import Optional, List
from ficsit.com.machines import Miner


class CompareRecipes:
    def __init__(self, item: str):
        self.item = item
        self.recipe_tree = load_recipes()
        self.all_paths = []
        self.graph = Graph()

    def _get_recipes(self, item: str) -> list:
        component_recipes = self.recipe_tree.get(item)
        if component_recipes:
            return component_recipes

        else:
            return None

    def build_all_alternates(self):

        for alternate in self._get_recipes(self.item):
            self.build_graph(alternate, self.item, None)

        print("built")

    def build_graph(self, produced_recipe: dict, child_node_name: str, parent_node:Optional[Node], component_name: Optional[str]=None):
        """
        Builds the graph for the given recipe
        """

        current_node = Node(child_node_name, produced_recipe)

        if parent_node is None:
            self.graph.add_root(current_node)
        else:
            self.graph.attach_child(parent_node, current_node, component_name)
        
 
        components = produced_recipe.get("components")

        for component, amount in components.items():
            next_recipes = self._get_recipes(component)
            if next_recipes is None or component in GameComponents.endpoints:
                component_child = self.graph.attach_child(current_node, self._create_component_node(component, amount), "Base Component")
                self.graph.define_endpoint(component_child)
                continue
            for child_recipe in next_recipes:
                if self._prevent_infinite_loops(current_node, child_recipe):
                    continue
                
                self.build_graph( child_recipe, component, current_node, component)
                
    def build_display_paths(self) -> List[str]:
        """
        Builds an output of all unique paths from the recipe to the base components.
        """


        output = ([self.format_display_path(path[-1].path_to_root) for path in self.graph.all_paths_to_root])
        return output
        #return list(set(output))


    def format_display_path(self, path: List[Node]) -> str:
        """
        formats a display path from start to end.

        formats it as "Display_Name (Component + Component + Component...) -> Next_Node (Component + Component)
        """

        complete_path = []
        for i, node in enumerate(path):
            recipe_name = node.display_name
            if i != 0 and node.components_per_cycle is not None:
                recipe_name = f"[{display_name(node.NODE_NAME)}] {recipe_name}" 
                
            if node.components_per_cycle is not None:
                components = ' + '.join([display_name(component) for component in node.components_per_cycle])
                components = f" ({components})"
            else:
                components = ""
            complete_path.append(f"{recipe_name}{components}")
            
    
        return " -> ".join(complete_path)


    def record_path(self, path: list, components: dict) -> str:

        component_string = self.add_base_components_string(
            components, " -> Resource Node"
        )

        self.all_paths.append(f"{' -> '.join(path)} {component_string}")

            
    def _prevent_infinite_loops(self, current_node: Node, next_recipe: str):
        current_chain = [node.display_name for node in current_node.path_to_root]
        current_chain.append(next_recipe['recipeName'])
        reduced_chain = list(set(current_chain))

        return len(current_chain) != len(reduced_chain)

            

    def _is_all_components(self, ingredients: dict) -> bool:

        for ingredient in ingredients:
            if ingredient not in GameComponents.endpoints:
                return False

        return True

    def _create_component_node(self, component: str, amount: int):
        """
        wrapper for creating a node for the graph that is just a component
        """
        return Node(
            component,
            NodeProps(
                recipeName= display_name(component),
                producesPerCycle=amount,
                producedIn=Miner,
                components=None,
                componentsPerMinute=None,
                cycleTime=0,
                cyclesPerMinute=0,
                manualMultiplier=0
            )
        )

    def add_base_components_string(self, ingredients: dict, separator: str) -> str:

        string = ""
        for component in ingredients:
            string += f"{display_name(component)} + "

        return f"{separator} ({string[:-3]})" if len(ingredients) > 0 else ""
