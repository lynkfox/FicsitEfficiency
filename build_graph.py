from ficsit2.com.graph import Graph
from ficsit2.com.node import RecipeNode, ComponentNode
from ficsit2.com.names import ComponentName
import json


class ProductionChain:
    def __init__(self, name: ComponentName):
        self.component = name
        self.name = name.value

        self._init_production_chain_graph()

    def load_recipes(self):
        with open("./ficsit2/data/recipes.json") as file:
            return json.load(file)

    def _init_production_chain_graph(self) -> Graph:
        """
        Builds a Production chain graph for a given recipe
        """
        self.graph = Graph(
            root=ComponentNode(ComponentName(self.name), recipe_needs=1.0),
            recipe_tree=self.load_recipes(),
        )

    def __str__(self) -> str:
        return str(self.graph.root)


def main():
    chain = ProductionChain(name=ComponentName.COPPER_SHEET)

    print(chain)


if __name__ == "__main__":
    main()
