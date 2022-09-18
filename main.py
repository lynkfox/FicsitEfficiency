from ficsit.effeciency import CompareRecipies
import json
from ficsit.components import (
    Equipment,
    ManufacturedComponents,
    ProjectAssemblyPart,
    Ingots,
    display_name_mapping,
    endpoints,
)


def main(recipe_name):
    setup_class = CompareRecipies(recipe_name)

    recipes = setup_class.get_all_recipe_paths_to_base_component()

    display_name = display_name_mapping.get(recipe_name, recipe_name)
    output = {"item": display_name, "totalPaths": len(recipes), "allPaths": recipes}

    filename = display_name.lower().replace(" ", "_")

    with open(f"./ficsit/possible_paths/{filename}.json", "w") as json_file:
        json.dump(output, json_file)


if __name__ == "__main__":

    for key in display_name_mapping:
        if key not in endpoints:
            main(key)
