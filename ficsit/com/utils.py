import json
from ficsit.com.components import display_name_mapping


def load_recipes():
    with open("./ficsit/recipes/recipes.json") as file:
        return json.load(file)


def display_name(component: str):
    """
    returns the display name of a given component
    """
    return display_name_mapping.get(component, component)
