from ficsit2.com.names import ComponentName
from ficsit2.com import lookup
from ficsit2.chain.production_chain import ProductionChain
from ficsit2.mod_input.mod_include import ModdedContent
import argparse
from time import perf_counter
import json


# Here to help running the debugger
DEBUG_COMPONENT = ComponentName("Copper Sheet")

DECIMAL_FORMAT = "{:.3f}"

parser = argparse.ArgumentParser(description="Builds and outputs the Efficiency Graph.")
parser.add_argument(
    "--component",
    "-c",
    help="What component to run this against. See .ficsit2/com/names.py ComponentNames for a list of names - use the pretty name (right side)",
)
parser.add_argument(
    "--verbose",
    "-v",
    action="count",
    default=0,
    help="Gives more information on output. Can be used twice, -vvv, third use prints out the entire graph (dont use with -all!)",
)
parser.add_argument(
    "--all",
    "-a",
    action="store_true",
    help="Builds the tree output for ALL Components. WARNING CAN TAKE QUITE A BIT OF TIME",
)

parser.add_argument(
    "--produce",
    "-p",
    type=float,
    default=1.0,
    help="How many of the root component to produce/min. Defaults to 1/min",
)

args = parser.parse_args()

COMPONENT = args.component if args.component is not None else DEBUG_COMPONENT

PRODUCE = args.produce


def main(map_this_component: ComponentName, mod_content, recipes_last_generated):

    start = perf_counter()

    output_location = (
        "./output/recipe_comparison_trees/" if PRODUCE == 1 else "./output/user/"
    ) + f"{map_this_component.name.lower()}.txt"

    last_generated_line = f"Based on Recipes Generated On: {recipes_last_generated}\n"

    if PRODUCE == 1:
        try:
            with open(output_location, "r") as file:
                first_line = file.readline()
        except:
            first_line = None

        if first_line == last_generated_line:
            print(
                f"No change to {map_this_component.name.lower()}.txt since last generated. Skipping"
            )
            return

    chain = ProductionChain(
        name=map_this_component, how_many=PRODUCE, modded=mod_content
    )

    if args.verbose != 3:
        with open(output_location, "w") as recipe_file:
            recipe_file.write(f"{last_generated_line}\n" + str(chain))

    if args.verbose >= 3:
        print(chain)

    if args.verbose >= 1:
        print(
            f"{map_this_component.value} complete in {DECIMAL_FORMAT.format(perf_counter()-start)} seconds."
        )

    if args.verbose >= 2:
        print(
            f"    - {chain.graph.total_depth/2} layers, {len(chain.graph.paths_to_root)} paths to a raw resource."
        )


if __name__ == "__main__":
    start = perf_counter()
    total = 1

    with open("./ficsit2/data/recipes.json", "r") as json_file:
        recipes_last_generated = json.load(json_file).get("last_generated")

    mod_content = ModdedContent()
    if args.all:
        print(
            "Running all recipes: May take up to 30 seconds **per component being calculated**"
        )
        for component in ComponentName:
            if component not in lookup.ENDPOINTS:
                main(component, mod_content, recipes_last_generated)
                total += 1

        for mod_component in mod_content.component:
            main(mod_component, mod_content, recipes_last_generated)
            total += 1
    else:
        try:
            use_this = ComponentName(COMPONENT)
        except Exception:

            for mod_component in mod_content.component:
                if mod_component.value == COMPONENT:
                    use_this = mod_component
                    break

        main(use_this, mod_content, recipes_last_generated)

    print(
        f"\n\033[92mDone in {DECIMAL_FORMAT.format(perf_counter()-start)} seconds and {total} starting points.\033[0m"
    )
