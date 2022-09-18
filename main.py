from ficsit.effeciency import CompareRecipes
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
    display_name = display_name_mapping.get(recipe_name, recipe_name)

    print(f"Creating document for {display_name}")
    setup_class = CompareRecipes(recipe_name)

    setup_class.build_all_alternates()
    recipe_paths = setup_class.build_display_paths()

    
    output = {"item": display_name, "totalPaths": len(recipe_paths), "allPaths": recipe_paths}

    filename = display_name.lower().replace(" ", "_")

    with open(f"./ficsit/possible_paths/{filename}.json", "w") as json_file:
        json.dump(output, json_file, indent=4)

    del display_name

if __name__ == "__main__":

    for key in display_name_mapping:
        if key not in endpoints:
            main(key)
