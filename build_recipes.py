import json
from xml.etree import ElementTree
from ficsit2.com.names import ComponentName as ComponentName
from ficsit2.com.recipe import Component
from ficsit2.com import lookup
from ficsit2.mod_input.mod_load import generate_all_modded_recipes
import argparse
from datetime import datetime
from dateutil import tz
from ficsit2.com.lookup import COMPONENT_MAPPING, MACHINE_MAPPING

parser = argparse.ArgumentParser(
    description="Build the recipe.json that is consumed in the Efficiency Graph creation."
)
parser.add_argument(
    "--modded",
    "-m",
    action="store_true",
    help="Include modded content: see Readme for how to add modded content",
)

args = parser.parse_args()


def load_xml():
    with open("./ficsit2/data/RecipeTable.xml") as file:
        xml = ElementTree.parse(file)

    return xml


def get_recipes(xml_tree):

    all_buildables = xml_tree.findall(".//Recipe")

    all_recipes = {}

    for buildable in all_buildables:
        name = buildable.find("DisplayName")

        if name is None:
            continue

        if name.text in lookup.FICSMAS_RECIPES:
            print(f"\033[96m Xmas Recipe\033[0m {name.text} - skipped ")
            continue

        if name.text in lookup.IGNORED_RECIPES:
            print(f"\033[92m Recipe\033[0m {name.text} - skipped ")
            continue

        recipe = get_recipe_details(buildable, name.text)

        if recipe is None:
            continue

        components_produced = [
            COMPONENT_MAPPING.get(clean_item_name(item.attrib["item"]))
            for item in buildable.findall("Products/ItemAmount")
        ]
        if len(components_produced) != 0 and components_produced.count(None) != len(
            components_produced
        ):
            recipe["products"] = [x.value for x in components_produced]
        else:
            print(f"\033[93m++++WARNING,\033[0m {name.text} has 0 Components Produced")
            continue

        for component in components_produced:
            if component is None:
                print(f"*???Look Into: {recipe.get('recipeName')} is broken")
                continue
            if component.value in all_recipes:
                all_recipes[component.value].append(recipe)

            else:
                entry = {component.value: [recipe]}

                all_recipes.update(entry)

    print(
        f"\n\033[92m Main Recipe file done\033[0m with {len(all_recipes)} root components\n...applying additional Updated U6 Recipes and specific fixes..."
    )
    updated = integrate_update_6_changes(all_recipes)
    print(f"\n Done! {updated} recipes added/updated.")

    if args.modded:
        print("\n\033[93m Adding Modded Recipes...\033[0m")
        # TODO: loop over input/modded/* jsons
        modded = generate_all_modded_recipes(all_recipes)
        print(f"\n Done! {modded} modded recipes added/updated.")

    print(
        "\n\033[92m Skipped Recipes\033[0m are all either not crafted in Machines or have updated values in update_6_changes.json"
    )
    print(
        f"\033[96m Xmas Recipe\033[0m are skipped as there are 0 alternate chains for them, making efficiency discovery pointless"
    )
    print(
        "\n\033[93m Done. You do not need to run this script again unless new recipes added in ./ficsit2/data\033[0m\n"
    )

    return all_recipes


def clean_item_name(name):
    removed_ixs = name.split("_")
    small_name = (
        "".join(removed_ixs[1:-1])
        .replace("ItemDescriptor", "")
        .replace("EquipmentDescriptor", "")
    )

    return small_name[0].lower() + small_name[1:]


def get_recipe_details(buildable, name):

    produced_in = buildable.findall(".//ProducedIn/string")

    machine = None
    for source in produced_in:
        producers = source.text.split("/")
        producer = producers[-2].replace("Mk1", "") if len(producers) > 2 else None
        if producer not in MACHINE_MAPPING.keys():
            continue
        else:
            machine = MACHINE_MAPPING.get(producer)

    if machine is None or "unpackage" in name.lower():
        return None

    produced_amount = int(buildable.find(".//Products/ItemAmount").attrib["amount"])
    cycle_time = int(buildable.find("ManufactoringDuration").text)

    return {
        "recipeName": name if "Alternate:" in name else f"Standard: {name}",
        "producedIn": machine.name.value,
        "producesPerCycle": produced_amount,
        "components": build_components(buildable.findall(".//Ingredients/ItemAmount")),
        "cycleTime": cycle_time,
        "products": [],
    }


def build_components(ingredients) -> list:

    all_components = []

    for ingredient in ingredients:
        name = COMPONENT_MAPPING.get(clean_item_name(ingredient.attrib["item"]))
        if name is None:
            print(
                f"\033[93m*****WARNING,\033[0m {ingredient.attrib['item']} not found in COMPONENT_MAPPING******"
            )
            continue
        amount = int(ingredient.attrib["amount"])
        is_fluid = name in lookup.FLUIDS

        all_components.append(
            Component(name=name, amount=amount / 100 if is_fluid else amount).as_dict()
        )

    return all_components


def integrate_update_6_changes(original_recipes: dict):
    """
    Loads in the u6 recipes and recipe changes
    """

    with open(f"./ficsit2/data/update_6_changes.json", "r") as json_file:
        additional_recipes = json.load(json_file)

    added = 0
    for recipe_name, recipe in additional_recipes.items():

        if recipe_name in original_recipes.keys():
            original_recipes[recipe_name].extend(recipe)

        else:
            original_recipes[recipe_name] = recipe

        added += len(recipe)

    return added


def main():
    xml = load_xml()

    recipes = get_recipes(xml)

    with open("./ficsit2/data/recipes.json", "w") as json_file:
        recipes["last_generated"] = datetime.now(tz=tz.UTC).strftime(
            "%Y-%m-%d %H:%M:%S%Z"
        )
        json.dump(recipes, json_file, indent=4)


if __name__ == "__main__":

    main()
