from ficsit2.mod_input.mod_item import *


def is_content_lib(object: dict) -> bool:
    """
    determines if a particular dictionary object is a content lib object or not.
    """

    return "ContentLib" in object.get("$schema", "")


def translate_content_lib_recipe(object: dict, mod_name: str, new_items: dict) -> dict:
    """
    Converts a content lib recipe format into ficsit efficiency internal format.

    Any new items or buildings are added to the new_items dict by reference
    """

    produced_items = [
        handle_potential_mod_product(new_items, product)
        for product in object["Products"]
    ]

    output = {}
    for product_name, amount in produced_items:
        output[product_name] = [
            {
                "recipeName": f"{mod_name.replace('/', '')}: {object['Name']}",
                "producedIn": handle_potential_mod_buildings(
                    new_items, object["ProducedIn"][0]
                ),
                "producesPerCycle": amount,
                "components": [
                    handle_potential_mod_ingredient(new_items, ingredient)
                    for ingredient in object["Ingredients"]
                ],
                "cycleTime": object["ManufacturingDuration"],
                "products": [name for name, _ in produced_items],
            }
        ]

    return output
