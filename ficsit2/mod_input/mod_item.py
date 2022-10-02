from ficsit2.com.lookup import MACHINE_MAPPING, COMPONENT_MAPPING
from typing import Tuple
from ficsit2.com.lookup import FLUIDS


def handle_potential_mod_product(new_items: dict, product: dict) -> Tuple[str, int]:
    """
    returns the name of the item being produced to align with ficsit/efficiency and the amount of the item.
    """
    name = record_modded_item(
        new_items, product.get("Item"), type="items", mapping=COMPONENT_MAPPING
    )
    amount, _ = determine_item_amount(product, name)

    return name, amount


def handle_potential_mod_ingredient(new_items: dict, ingredient: dict) -> dict:
    """
    deal with mod added ingredients that are known list, updating the passed new_items dict by ref and returning
    the ingredient as a component dictionary.
    """

    name = record_modded_item(
        new_items, ingredient.get("Item"), type="items", mapping=COMPONENT_MAPPING
    )
    amount, measurement = determine_item_amount(ingredient, name)

    return {
        "name": name,
        "amount": amount,
        "measurement": measurement + "/productionCycle",
    }


def handle_potential_mod_buildings(new_items: dict, building: str) -> str:
    """
    Deals with mod added buildings that are not in the known list, updating by ref the passed new_items dict
    and returning the name of the building (prefixing with MOD_ if not found in known buildings)
    """
    return record_modded_item(
        new_items, building, type="machines", mapping=MACHINE_MAPPING
    )


def determine_item_amount(item: dict, name: str) -> Tuple[int, str]:
    """
    cleans up the amount if fluid, otherwise just returns as is. Also returns the measurement string qualifier
    """
    amount = item.get("Amount")
    measurement = "items"
    if name in FLUIDS or amount > 1000:
        amount = amount / 1000
        measurement = "m^3"
    return amount, measurement


def record_modded_item(new_items: dict, item: any, type: str, mapping: dict):
    """
    records the new item appropriately and returns its name for the output
    """
    name = clean_content_lib_names(item)

    if type == "machines":
        ### yyyy this is such a hack and im too lazy to go fix the root issue!
        name = name[0].upper() + name[1:]

    known = mapping.get(name)

    if known is None:
        name = "Modded: " + camel_case_split(name)
        new_items[type].append(name.replace("  ", " "))

    else:
        name = known.name.value if type == "machines" else known.value

    return name


def clean_content_lib_names(str) -> str:
    """
    Takes names from Content Lib and cleans them up for use against mapping files
    """
    removed_prefix = (
        str.replace("Desc_", "").replace("Build_", "").replace("Mk1", "").strip()
    )

    return removed_prefix[0].lower() + removed_prefix[1:]


def camel_case_split(str):
    """
    splits camelCase or PascalCase into camel Case | Pascal Case strings
    """
    new_string = ""
    for i in str:
        if i.isupper():
            new_string += "*" + i
        else:
            new_string += i
    x = new_string.split("*")
    if x[0] == "":
        x = x[1:]
    return " ".join([word.capitalize() for word in x])
