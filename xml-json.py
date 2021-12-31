import json
from xml.etree import ElementTree


def load_xml():
    with open("./ficsit/recipes/RecipeTable.xml") as file:
        xml = ElementTree.parse(file)

    return xml


def get_recipes(xml_tree):

    all_buildables = xml_tree.findall(".//Recipe")

    all_recipes = {}

    for buildable in all_buildables:
        name = buildable.find("DisplayName")

        if name is None:
            continue

        recipe = get_recipe_details(buildable, name.text)

        if recipe is None:
            continue

        components_produced = [clean_item_name(
            item.attrib["item"]) for item in buildable.findall("Products/ItemAmount")]

        for component in components_produced:

            if component in all_recipes:
                all_recipes[component].append(recipe)

            else:
                entry = {
                    component: [recipe]
                }

                all_recipes.update(entry)

    # add Nuclear Waste from Powerplant

    nuclearWaste = {
        "nuclearWaste": [
            {
                "recipeName": "Nuclear Waste",
                "producedIn": "Nuclear Power Plant",
                "produces": 50,
                "components": {
                    "nuclearFuelRod": 1,
                    "water": 1500
                },
                "timeToProduce": 300,
                "manualMultiplier": 0.0
            }
        ]}

    all_recipes.update(nuclearWaste)

    return all_recipes


def get_recipe_details(buildable, name):

    produced_in = buildable.findall(".//ProducedIn/string")

    MACHINES = ["Smelter", "Foundry", "Constructor", "Assembler",
                "Manufacturer", "OilRefinery", "Blender", "Packager", "HadronCollider"]

    machine = None

    for source in produced_in:
        producers = source.text.split("/")
        producer = producers[-2].replace("Mk1",
                                         "") if len(producers) > 2 else None
        if producer not in MACHINES:
            continue
        else:
            if producer == "HadronCollider":
                machine = "ParticleAccelerator"
            else:
                machine = producer

    if machine is None or "unpackage" in name.lower():
        return None

    return {
        "recipeName": name,
        "producedIn": machine,
        "produces": int(buildable.find(".//Products/ItemAmount").attrib['amount']),
        "components": {clean_item_name(ingredient.attrib['item']): int(ingredient.attrib['amount']) for ingredient in buildable.findall(".//Ingredients/ItemAmount")},
        "timeToProduce": int(buildable.find("ManufactoringDuration").text),
        "manualMultiplier": float(buildable.find("ManualManufacturingMultiplier").text)
    }


def clean_item_name(name):
    removed_ixs = name.split("_")
    small_name = "".join(
        removed_ixs[1:-1]).replace("ItemDescriptor", "").replace("EquipmentDescriptor", "")

    return small_name[0].lower() + small_name[1:]


def main():
    xml = load_xml()

    recipies = get_recipes(xml)

    with open("./ficsit/recipes/recipes.json", "w") as json_file:
        json.dump(recipies, json_file)


if __name__ == "__main__":

    main()
