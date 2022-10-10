from ficsit2.com.names import ComponentName
from ficsit2.com import lookup
from ficsit2.chain.production_chain import ProductionChain
import argparse
from ficsit2.mod_input.mod_include import ModdedContent
from time import perf_counter
import json


# Here to help running the debugger
DEBUG_COMPONENT = ComponentName.HEAVY_MODULAR_FRAME

DECIMAL_FORMAT = "{:.3f}"

parser = argparse.ArgumentParser(
    description="Builds and outputs the Production Chains."
)
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
    help="Gives more information on output. Can be used twice, -vvv, third use prints out every chain (dont use with -all!)",
)
parser.add_argument(
    "--all",
    "-a",
    action="store_true",
    help="Builds the tree output for ALL Components. WARNING CAN TAKE QUITE A BIT OF TIME",
)


args = parser.parse_args()

COMPONENT = args.component if args.component is not None else DEBUG_COMPONENT


def main(map_this_component: ComponentName, mod_content, chain_last_generated):

    start = perf_counter()

    output_location = (
        "./output/production_chains/" + f"{map_this_component.name.lower()}.txt"
    )

    try:
        with open(output_location, "r") as file:
            first_line = file.readline()
    except:
        first_line = None

    last_generated_line = f"Based on Recipes Generated On: {chain_last_generated}\n"
    if first_line == last_generated_line:
        print(
            f"No change to {map_this_component.name.lower()}.txt since last generated. Skipping"
        )
        return

    chain = ProductionChain(name=map_this_component, how_many=1, modded=mod_content)
    all_production_chains = chain.build_production_chains()

    if args.verbose != 3:
        with open(output_location, "w") as recipe_file:
            recipe_file.write(
                f"{last_generated_line}\n" + "\n".join(all_production_chains)
            )

    if args.verbose >= 3:
        print(all_production_chains)

    if args.verbose >= 1:
        print(
            f"{map_this_component.value} complete in {DECIMAL_FORMAT.format(perf_counter()-start)} seconds."
        )

    if args.verbose >= 2:
        print(f"    - {len(all_production_chains)} paths to a raw resource.")


if __name__ == "__main__":
    start = perf_counter()
    total = 1
    mod_content = ModdedContent()

    with open("./ficsit2/data/recipes.json", "r") as json_file:
        chains_last_generated = json.load(json_file).get("last_generated")

    if args.all:
        print("Running Production Chains for all recipes: May take up to 30 seconds")
        for component in ComponentName:
            if component not in lookup.ENDPOINTS:
                main(component, mod_content, chains_last_generated)
                total += 1

        for mod_component in mod_content.component:
            main(mod_component, mod_content, chains_last_generated)
            total += 1
    else:
        try:
            use_this = ComponentName(COMPONENT)
        except Exception:

            for mod_component in mod_content.component:
                if mod_component.value == COMPONENT:
                    use_this = mod_component
                    break

        main(use_this, mod_content, chains_last_generated)

    print(
        f"\n\033[92mDone in {DECIMAL_FORMAT.format(perf_counter()-start)} seconds and {total} starting points.\033[0m"
    )
