from ficsit.utils import load_recipes
from ficsit import components as GameComponents

class CompareRecipies():
    def __init__(self, item: str):
        self.item = item
        self.recipe_tree = load_recipes()
        self.all_paths = []

    def _get_recipes(self, item: str)-> list:
        component_recipes = self.recipe_tree.get(item)
        if component_recipes:
            return component_recipes

        else:
            return None

    def get_all_recipe_paths_to_base_component(self, base_component):

        path = []

        self._get_recipe_paths(self._get_recipes(self.item)[0], base_component, path)
         
        return self.all_paths

    def _get_recipe_paths(self, produced_recipe:dict, base_component: str, path: list) -> list:

        recipe_name = produced_recipe.get("recipeName")
        path.append(recipe_name) 
        

        components = produced_recipe.get("components")

        for component in components.keys():
            if component in GameComponents.endpoints:
                self.all_paths.append(self._display_path(path, component))
            else:
                next_recipes = self._get_recipes(component)

                if next_recipes is None:
                    continue
                else:
                    for child_recipe in next_recipes:
                        if child_recipe.get("recipeName") not in path:
                            self._get_recipe_paths(child_recipe, base_component, path)
                            path = path[:-1]


    def _display_path(self, path: list, endpoint) -> str:

        return f"{GameComponents.display_name_mapping.get(self.item)} > {' > '.join(path)} > {GameComponents.display_name_mapping.get(endpoint)}" 