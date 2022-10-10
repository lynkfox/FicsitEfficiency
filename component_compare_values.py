from ficsit2.chain.chain_graph import ChainGraph
import argparse
from ficsit2.com.names import ComponentName
from ficsit2.mod_input.mod_include import ModdedContent
from ficsit2.com.recipe import load_recipes

DEBUG_COMPONENT = ComponentName.HEAVY_MODULAR_FRAME

parser = argparse.ArgumentParser(
    description="Builds and outputs the Production Chains."
)
parser.add_argument(
    "--component",
    "-c",
    help="What component to run this against. See .ficsit2/com/names.py ComponentNames for a list of names - use the pretty name (right side)",
)

recipe_arguments = parser.add_mutually_exclusive_group()

recipe_arguments.add_argument(
    "--standard",
    "-s",
    help="Skip recipe selection and only use standard",
    action="store_true",
)
recipe_arguments.add_argument(
    "--file",
    "-f",
    help="name of the file containing the selected recipes and components, located in ./input/compare/*",
)

args = parser.parse_args()

COMPONENT = (
    ComponentName(args.component) if args.component is not None else DEBUG_COMPONENT
)

def main():
    recipes = load_recipes()
    mod_content = ModdedContent()
    single_product = ChainGraph(COMPONENT, recipes, mod_content=mod_content, use_standard=args.standard)
    print(single_product.str_comparison())

if __name__ == "__main__":
    main()