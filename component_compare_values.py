from ficsit2.chain.chain_graph import ChainGraph
import argparse
from ficsit2.com.names import ComponentName
from ficsit2.mod_input.mod_include import ModdedContent
from ficsit2.com.recipe import load_recipes
import re
import json
from datetime import datetime

DEBUG_COMPONENT = ComponentName.HEAVY_MODULAR_FRAME

parser = argparse.ArgumentParser(
    description="Builds and outputs the Production Chains."
)
parser.add_argument(
    "--component",
    "-c",
    help="What component to run this against. See .ficsit2/com/names.py ComponentNames for a list of names - use the pretty name (right side)",
)
parser.add_argument(
    "--saveOutput",
    "-s",
    action="store_true",
    help="Save the output in .output/user. shares the same suffix as --r, can specify name with --f",
)
parser.add_argument(
    "--recipesSave",
    "-r",
    action="store_true",
    help="Save the recipes chosen in .output/user. shares the same suffix as --s, can specify with --f",
)
parser.add_argument(
    "--quiet",
    "-q",
    action="store_true",
    help="suppresses the output of the final value to the terminal",
)
parser.add_argument(
    "--fileSuffix",
    "-f",
    help="name of the file containing the selected recipes and components, located in ./input/compare/*",
)

recipe_arguments = parser.add_mutually_exclusive_group()

recipe_arguments.add_argument(
    "--onlyStandard",
    "-o",
    help="Skip recipe selection and only use standard",
    action="store_true",
)
recipe_arguments.add_argument(
    "--inputFile",
    "-i",
    help="name of the json file containing the selected recipes and components, located in ./output/user/*",
)

args = parser.parse_args()

COMPONENT = (
    ComponentName(args.component) if args.component is not None else DEBUG_COMPONENT
)


STRING_CLEANUP = {
    "\033[95m": "",
    "\033[94m": "",
    "\033[96m": "",
    "\033[92m": "",
    "\033[93m": "",
    "\033[91m": "",
    "\033[0m": "",
    "\033[1m": "",
    "\033[4m": "",
}


def main():
    recipes = load_recipes()
    mod_content = ModdedContent()
    starting_recipes = {}
    if args.inputFile is not None:
        with open(f"./output/user/{args.inputFile}") as file:
            starting_recipes = json.load(file)

    single_product = ChainGraph(
        COMPONENT,
        recipes,
        recipes_selected=starting_recipes,
        mod_content=mod_content,
        use_standard=args.onlyStandard,
    )
    result = single_product.str_comparison()
    based_on = recipes["last_generated"]

    if args.fileSuffix is not None:
        extra = args.fileSuffix.replace(" ", "_").lower()
    else:
        extra = datetime.now().strftime("%Y%m%d%H%M%S")
    output_location = f"./output/user/{COMPONENT.name.lower()}"
    generated_on = f"Based on Recipes generated on {based_on}"

    if not args.quiet:
        print(result)

    if args.saveOutput:
        save_output(result, f"{output_location}_{extra}", generated_on)

    if args.recipesSave:
        file_name = f"{output_location}_{extra}.json"
        with open(file_name, "w") as json_file:
            print(f"\n\033[93mSaving recipes used to {file_name}\033[0m")
            json.dump(single_product.save_recipes(), json_file, indent=4)

    print("\n\033[1mAll Done!\033[0m\n\n")


def save_output(result, output_location, generated_on):
    """
    cleans up and removes the bash colors, then saves the output
    """
    result = clean_string(result, STRING_CLEANUP)
    file_name = output_location + ".txt"
    with open(file_name, "w") as file:
        print(f"\n\033[96mSaving comparison output to {file_name}\033[0m")
        file.write(f"{generated_on}\n" + result)


def clean_string(result, mapping):
    rep = dict((re.escape(k), v) for k, v in mapping.items())
    pattern = re.compile("|".join(rep.keys()))
    result = pattern.sub(lambda m: rep[re.escape(m.group(0))], result)
    return result


if __name__ == "__main__":
    main()
