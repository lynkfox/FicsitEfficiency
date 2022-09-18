from ficsit.utils import load_recipes
from ficsit import components as GameComponents
from functools import reduce
from ficsit.com.graph_node import Graph, Node
from typing import Optional


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

    def get_all_recipe_paths_to_base_component(self):

        path = []

        for alternate in self._get_recipes(self.item):
            self.build_graph(alternate, self.item, None)
        # for alternate in self._get_recipes(self.item):
        #     self._get_recipe_paths(alternate, path, self.item, None)
        #     path = []

        return self.all_paths

    def build_graph(self, produced_recipe: dict, child_node_name: str, parent_node:Optional[Node]):
        """
        Builds the graph for the given recipe
        """
        current_node = None
        recipe_name = produced_recipe.get("recipeName")
        if parent_node is None:
            current_node = Node(self.item, produced_recipe)
            self.graph.add_root(current_node)

        else:
            current_node = Node(child_node_name, produced_recipe)
            parent_node.add_child(current_node)
            self.graph.Nodes[current_node.ID] = current_node
        
        self.graph.max_depth = current_node.depth if current_node.depth > self.graph.max_depth else self.graph.max_depth

        components = produced_recipe.get("components")

        for component in components.keys():
            next_recipes = self._get_recipes(component)
            if next_recipes is None or component in GameComponents.endpoints:
                continue
            else:
                for child_recipe in next_recipes:
                    self.build_graph( child_recipe, component, current_node )

    def _get_recipe_paths(
        self, produced_recipe: dict, path: list, item_name: str, parent_node: Optional[Node]
    ) -> list:

        current_node = None
        recipe_name = produced_recipe.get("recipeName")
        if item_name == self.item:
            recipe_name = f"[{recipe_name}]"
            current_node = Node(self.item, produced_recipe)
            self.graph.add_root(current_node)

        else:
            
            current_node = Node(item_name, produced_recipe)
            current_node.add_parent(parent_node)
            parent_node.add_child(current_node)
            current_node.depth = parent_node.depth+1
            self.graph.Nodes[current_node.ID] = current_node
            recipe_name = f"{item_name}[{recipe_name}]"

        if current_node.depth > self.graph.max_depth:
            self.graph.max_depth = current_node.depth

        path.append(self.display_name(item_name))

        components = produced_recipe.get("components")

        for component in components.keys():
            if self._is_all_components(components):
                self.record_path(path, components)
                break
            else:
                next_recipes = self._get_recipes(component)

                if next_recipes is None or component in GameComponents.endpoints:
                    continue
                else:
                    for child_recipe in next_recipes:
                        if child_recipe.get("recipeName") not in str(path):
                            path[-1] += (
                                self.add_base_components_string(components, "")
                                if path[-1][-1] != ")"
                                else ""
                            )
                            self._get_recipe_paths(
                                child_recipe, path, component, current_node
                            )
                            del path[-1]

    def display_name(self, component):
        return GameComponents.display_name_mapping.get(component, component)

    def record_path(self, path: list, components: dict) -> str:

        component_string = self.add_base_components_string(
            components, " -> Resource Node"
        )

        self.all_paths.append(f"{' -> '.join(path)} {component_string}")

    def _is_all_components(self, ingredients: dict) -> bool:

        for ingredient in ingredients:
            if ingredient not in GameComponents.endpoints:
                return False

        return True

    def add_base_components_string(self, ingredients: dict, separator: str) -> str:

        string = ""
        for component in ingredients:
            string += f"{self.display_name(component)} + "

        return f"{separator} ({string[:-3]})" if len(ingredients) > 0 else ""
