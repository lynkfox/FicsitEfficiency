import json
from xml.etree import ElementTree
from ficsit2.com.machines import machine_map
from ficsit2.com.names import Buildable, ComponentName as ComponentName
from ficsit2.com.recipe import Component
from ficsit2.com import lookup
import argparse

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

MACHINE_MAPPING = {
    "Smelter": machine_map.get(Buildable.SMELTER),
    "Foundry": machine_map.get(Buildable.FOUNDRY),
    "Constructor": machine_map.get(Buildable.CONSTRUCTOR),
    "Assembler": machine_map.get(Buildable.ASSEMBLER),
    "Manufacturer": machine_map.get(Buildable.MANUFACTURER),
    "OilRefinery": machine_map.get(Buildable.REFINERY),
    "Blender": machine_map.get(Buildable.BLENDER),
    "Packager": machine_map.get(Buildable.PACKAGER),
    "HadronCollider": machine_map.get(Buildable.PARTICLE_ACCELERATOR),
}

COMPONENT_MAPPING = {
    "portableMiner": ComponentName.PORTABLE_MINER,
    "goldIngot": ComponentName.CATERIUM_INGOT,
    "steelIngot": ComponentName.STEEL_INGOT,
    "stone": ComponentName.LIMESTONE,
    "oreIron": ComponentName.IRON_ORE,
    "oreCopper": ComponentName.COPPER_ORE,
    "rawQuartz": ComponentName.RAW_QUARTZ,
    "coal": ComponentName.COAL,
    "sulfur": ComponentName.SULFUR,
    "oreGold": ComponentName.CATERIUM_ORE,
    "oreBauxite": ComponentName.BAUXITE_ORE,
    "oreUranium": ComponentName.URANIUM_ORE,
    "water": ComponentName.WATER,
    "liquidOil": ComponentName.OIL,
    "nitrogenGas": ComponentName.NITROGEN,
    "genericBiomass": ComponentName.BIOMASS,
    "wood": ComponentName.WOOD,
    "quartzCrystal": ComponentName.QUARTZ_CRYSTAL,
    "ironIngot": ComponentName.IRON_INGOT,
    "circuitBoardHighSpeed": ComponentName.AI_LIMITER,
    "aluminumPlate": ComponentName.ALCLAD_ALUMINUM_SHEET,
    "aluminumCasing": ComponentName.ALUMINUM_CASING,
    "aluminumIngot": ComponentName.ALUMINUM_INGOT,
    "aluminumScrap": ComponentName.ALUMINUM_SCRAP,
    "aluminaSolution": ComponentName.ALUMINA_SOLUTION,
    "battery": ComponentName.BATTERY,
    "gunpowder": ComponentName.BLACK_POWDER,
    "cable": ComponentName.CABLE,
    "circuitBoard": ComponentName.CIRCUIT_BOARD,
    "compactedCoal": ComponentName.COMPACTED_COAL,
    "computer": ComponentName.COMPUTER,
    "cement": ComponentName.CONCRETE,
    "coolingSystem": ComponentName.COOLING_SYSTEM,
    "copperDust": ComponentName.COPPER_POWDER,
    "copperIngot": ComponentName.COPPER_INGOT,
    "copperSheet": ComponentName.COPPER_SHEET,
    "crystalOscillator": ComponentName.CRYSTAL_OSCILLATOR,
    "electromagneticControlRod": ComponentName.ELECTROMAGNETIC_CONTROL_ROD,
    "steelPlateReinforced": ComponentName.ENCASED_INDUSTRIAL_BEAM,
    "plutoniumCell": ComponentName.ENCASED_PLUTONIUM_CELL,
    "uraniumCell": ComponentName.ENCASED_URANIUM_CELL,
    "fabric": ComponentName.FABRIC,
    "liquidFuel": ComponentName.FUEL,
    "modularFrameFused": ComponentName.FUSED_MODULAR_FRAME,
    "aluminumPlateReinforced": ComponentName.HEAT_SINK,
    "modularFrameHeavy": ComponentName.HEAVY_MODULAR_FRAME,
    "heavyOilResidue": ComponentName.HEAVY_OIL_RESIDUE,
    "highSpeedConnector": ComponentName.HIGH_SPEED_CONNECTOR,
    "ironPlate": ComponentName.IRON_PLATE,
    "ironRod": ComponentName.IRON_ROD,
    "modularFrame": ComponentName.MODULAR_FRAME,
    "motor": ComponentName.MOTOR,
    "nitricAcid": ComponentName.NITRIC_ACID,
    "nonFissibleUranium": ComponentName.NON_FISSILE_URANIUM,
    "nuclearWaste": ComponentName.URANIUM_WASTE,
    "petroleumCoke": ComponentName.PETROLEUM_COKE,
    "plastic": ComponentName.PLASTIC,
    "plutoniumFuelRod": ComponentName.PLUTONIUM_FUEL_ROD,
    "plutoniumPellet": ComponentName.PLUTONIUM_PELLET,
    "pressureConversionCube": ComponentName.PRESSURE_CONVERSION_CUBE,
    "polymerResin": ComponentName.POLYMER_RESIN,
    "highSpeedWire": ComponentName.QUICKWIRE,
    "ironPlateReinforced": ComponentName.REINFORCED_IRON_PLATE,
    "modularFrameLightweight": ComponentName.RADIO_CONTROL_UNIT,
    "rotor": ComponentName.ROTOR,
    "rubber": ComponentName.RUBBER,
    "ironScrew": ComponentName.SCREWS,
    "silica": ComponentName.SILICA,
    "stator": ComponentName.STATOR,
    "steelPlate": ComponentName.STEEL_BEAM,
    "steelPipe": ComponentName.STEEL_PIPE,
    "sulfuricAcid": ComponentName.SULFURIC_ACID,
    "computerSuper": ComponentName.SUPERCOMPUTER,
    "liquidTurboFuel": ComponentName.TURBO_FUEL,
    "motorLightweight": ComponentName.TURBO_MOTOR,
    "nuclearFuelRod": ComponentName.URANIUM_FUEL_ROD,
    "nuclearWaste": ComponentName.URANIUM_WASTE,
    "plutoniumWaste": ComponentName.PLUTONIUM_WASTE,
    "wire": ComponentName.WIRE,
    "spaceElevatorPart1": ComponentName.SMART_PLATING,
    "spaceElevatorPart2": ComponentName.VERSATILE_FRAMEWORK,
    "spaceElevatorPart3": ComponentName.AUTOMATED_WIRING,
    "spaceElevatorPart4": ComponentName.MODULAR_ENGINE,
    "spaceElevatorPart5": ComponentName.ADAPTIVE_CONTROL_UNIT,
    "spaceElevatorPart6": ComponentName.MAGNETIC_FIELD_GENERATOR,
    "spaceElevatorPart7": ComponentName.ASSEMBLY_DIRECTOR_SYSTEM,
    "spaceElevatorPart8": ComponentName.THERMAL_PROPULSION_ROCKET,
    "spaceElevatorPart9": ComponentName.NUCLEAR_PASTA,
    "mycelia": ComponentName.MYCELIA,
    "leaves": ComponentName.LEAVES,
    "flowerPetals": ComponentName.FLOWER_PETALS,
    "colorCartridge": ComponentName.COLOR_CARTRIDGE,
    "packagedNitrogenGas": ComponentName.PACKAGED_NITROGEN_GAS,
    "hazmatFilter": ComponentName.IODINE_INFUSED_FILTER,
    "filter": ComponentName.GAS_FILTER,
    "gasTank": ComponentName.EMPTY_TANK,
    "fluidCanister": ComponentName.EMPTY_CANISTER,
    "liquidBiofuel": ComponentName.LIQUID_BIOFUEL,
    "biofuel": ComponentName.SOLID_BIOFUEL,
}


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
        "\n\033[92m Main Recipe file done\033[0m applying additional Updated U6 Recipes and specific fixes..."
    )
    updated = update_with_another_recipe_json(all_recipes, "additional_recipes.json")
    print(f"\n Done! {updated} recipes added/updated.")

    if args.modded:
        print("\n\033[93m Adding Modded Recipes...\033[0m")
        # TODO: loop over ficist2/data/modded/* jsons
        modded = update_with_another_recipe_json(
            all_recipes, "modded/vanilla_extended.json"
        )
        print(f"\n Done! {modded} modded recipes added/updated.")

    print(
        "\n\033[92m Skipped Recipes\033[0m are all either not crafted in Machines or have updated values in additional_recipes.json"
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


def update_with_another_recipe_json(original_recipes: dict, file_name: str):
    """
    Loads in the u6 recipes and recipe changes
    """

    with open(f"./ficsit2/data/{file_name}", "r") as json_file:
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
        json.dump(recipes, json_file, indent=4)


if __name__ == "__main__":

    main()
