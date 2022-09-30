from ficsit2.com.graph import Graph
from ficsit2.com.node import ComponentNode
from ficsit2.com.names import ComponentName
from ficsit2.com import lookup
import json
import argparse
from time import perf_counter

# Here to help running the debugger
DEBUG_COMPONENT = ComponentName.HEAVY_MODULAR_FRAME

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
    type=int,
    default=1,
    help="How many of the root component to produce/min. Defaults to 1/min",
)

args = parser.parse_args()

COMPONENT = (
    ComponentName(args.component) if args.component is not None else DEBUG_COMPONENT
)

PRODUCE = args.produce 


class ProductionChain:
    def __init__(self, name: ComponentName):
        self.component = name
        self.name = name.value

        self._init_production_chain_graph()
        self.product_chains = self.graph.paths_to_root

    def load_recipes(self):
        with open("./ficsit2/data/recipes.json") as file:
            return json.load(file)

    def _init_production_chain_graph(self) -> Graph:
        """
        Builds a Production chain graph for a given recipe
        """
        self.graph = Graph(
            root=ComponentNode(
                ComponentName(self.name),
                parent_recipe_needs=PRODUCE,
            ),
            recipe_tree=self.load_recipes(),
        )

    def build_chain_outputs():
        """
        Outputs chains and their costs
        """

    def __str__(self) -> str:
        return "> " + str(self.graph.root)[4:]


def main(map_this_component: ComponentName):

    start = perf_counter()
    chain = ProductionChain(name=map_this_component)

    with open(f"./output/{map_this_component.name.lower()}.txt", "w") as recipe_file:
        recipe_file.write(str(chain))

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
    if args.all:
        print("Running all recipes: May take up to 30 seconds")
        for component in ComponentName:
            if component not in lookup.ENDPOINTS:
                main(component)
                total += 1
    else:
        main(COMPONENT)

    print(f"\n\033[92mDone in {DECIMAL_FORMAT.format(perf_counter()-start)} seconds and {total} starting points.\033[0m")