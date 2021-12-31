from ficsit.effeciency import CompareRecipies
import json
from ficsit.components import ManufacturedComponents


def main(recipe):
    setup_class = CompareRecipies(recipe)

    recipes = setup_class.get_all_recipe_paths_to_base_component()

    with open(f"./ficsit/recipes/{recipe}.json", "w") as json_file:
        json.dump(recipes, json_file)
    


if __name__ == "__main__":

    main(ManufacturedComponents.IRON_PLATE)
