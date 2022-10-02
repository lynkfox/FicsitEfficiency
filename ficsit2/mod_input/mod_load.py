import json
from os import listdir
from os.path import isfile
from typing import Dict, Optional, Tuple
import json
from ficsit2.mod_input.mod_recipe import *

MOD_RECIPES_DIRECTORY = "./input/modded"


def generate_all_modded_recipes(all_modded_recipes: dict) -> int:
    """
    Creates the outputs necessary for all modded recipes - the recipes, and all the new Items/Buildings

    returns total new recipes added and a dict of the new items and machines

    Saves the new items in ficsit2/data
    """
    out = load_modded_files()

    all_new_items = {"machines": [], "items": []}
    total_added = 0
    for key, value in out.items():
        for recipe in value:
            ready_recipes = (
                translate_content_lib_recipe(recipe, key, all_new_items)
                if is_content_lib(recipe)
                else recipe
            )
            total_added += combine_recipes_into_single_output(
                all_modded_recipes, ready_recipes
            )
    collapse_new_items(all_new_items)
    with open("./ficsit2/data/modded_items.json", "w") as json_file:
        json.dump(all_new_items, json_file, indent=4)

    return total_added


def combine_recipes_into_single_output(existing_recipes: dict, ready_recipes: dict):
    """
    combines two recipe dicts by their keys (the product name for that block) without overwriting existing recipes
    """
    added = 0
    for key, value in ready_recipes.items():
        if key in existing_recipes.keys():
            existing_recipes[key].extend(value)
        else:
            existing_recipes[key] = value

        added += len(value)

    return added


def collapse_new_items(new_items: dict):
    for key, value in new_items.items():
        new_items[key] = list(set(value))


def load_modded_files(
    directory: str = MOD_RECIPES_DIRECTORY, mod_files: Optional[dict] = None
) -> Dict[str, str]:
    """
    Scans the input/modded directory for any recipes and loads them according to type.
    """

    mod_dir_contents = [f for f in listdir(directory)]

    mod_files = {} if mod_files is None else mod_files

    key_name = directory.replace(MOD_RECIPES_DIRECTORY, "").replace("/", "")
    for object in mod_dir_contents:
        full_object_path = f"{directory}/{object}"
        if isfile(full_object_path):
            with open(full_object_path, "r") as json_file:
                file_content = json.load(json_file)
                if mod_files.get(key_name) is not None:
                    mod_files[key_name].append(file_content)
                else:
                    mod_files[key_name] = [file_content]

        else:
            {**mod_files, **load_modded_files(full_object_path, mod_files)}

    return mod_files


if __name__ == "__main__":

    generate_all_modded_recipes()
