from ficsit.utils import load_recipes
from ficsit import components as GameComponents
from functools import reduce
from ficsit.com.graph_node import Graph, Node


class CompareRecipies():
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
            self._get_recipe_paths(
                alternate, path, self.item)
            path = []

        return self.all_paths

    def _get_recipe_paths(self, produced_recipe: dict, path: list, item_name: str) -> list:

        recipe_name = produced_recipe.get("recipeName")
        if item_name == self.item:
            recipe_name = f"[{recipe_name}]"
            self.graph.add_root(Node(self.item, produced_recipe))
            
        else:            
            recipe_name = f"{item_name}[{recipe_name}]"

        path.append(recipe_name)

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
                            path[-1] += self.add_base_components_string(
                                components, "") if path[-1][-1] != ")" else ""
                            self._get_recipe_paths(
                                child_recipe, path, self.display_name(component))
                            del path[-1]

    def display_name(self, component):
        return GameComponents.display_name_mapping.get(component, component)

    def record_path(self, path: list, components: dict) -> str:

        component_string = self.add_base_components_string(
            components, " -> Resource Node")

        self.all_paths.append(
            f"{' -> '.join(path)} {component_string}")

    def _is_all_components(self, ingredients: dict) -> bool:

        for ingredient in ingredients:
            if ingredient not in GameComponents.endpoints:
                return False

        return True

    def add_base_components_string(self, ingredients: dict, seperator: str) -> str:

        string = ""
        for component in ingredients:
            string += f"{self.display_name(component)} + "

        return f"{seperator} ({string[:-3]})" if len(ingredients) > 0 else ""
