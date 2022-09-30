from ficsit2.com.graph import Graph
from ficsit2.com.node import ComponentNode
from ficsit2.com.names import ComponentName
from ficsit2.com import lookup
import json
import argparse
from time import perf_counter

# Here to help running the debugger
DEBUG_COMPONENT = ComponentName.HEAVY_MODULAR_FRAME

parser = argparse.ArgumentParser(description="Builds and outputs the Efficiency Graph.")
parser.add_argument(
    "--component",
    "-c",
    help="What component to run this against. See .ficsit2/com/names.py ComponentNames for a list of names - use the pretty name (right side)",
)
parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    help="Tells the script to also output the final graph to the terminal",
)
parser.add_argument(
    "--all",
    "-a",
    action="store_true",
    help="Builds the tree output for ALL Components. WARNING CAN TAKE QUITE A BIT OF TIME",
)

args = parser.parse_args()

COMPONENT = (
    ComponentName(args.component) if args.component is not None else DEBUG_COMPONENT
)


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
                parent_recipe_needs=10.0,
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

    if args.verbose:
        print(chain)

    print(
        f"{map_this_component.value} complete in {lookup.DECIMAL_FORMAT.format(perf_counter()-start)} seconds."
    )
    if args.verbose:
        print(
            "\n    - {chain.graph.total_depth/2} layers"
            + "\n    - {len(chain.graph.paths_to_root)} paths to a raw resource"
        )


if __name__ == "__main__":
    if args.all:
        for component in ComponentName:
            if component not in lookup.ENDPOINTS:
                main(component)
    else:
        main(COMPONENT)
