from ficsit2.com.graph import Graph
from ficsit2.com.node import ComponentNode, RecipeNode, _try_for_modded_component
from ficsit2.com.names import ComponentName
from ficsit2.mod_input.mod_include import ModdedContent
from typing import List, Union, Optional
from ficsit2.com.recipe import load_recipes


class ProductionChain:
    def __init__(
        self,
        name: ComponentName,
        how_many: int = 1,
        modded: Optional[ModdedContent] = None,
    ):
        self.component = name
        self.name = name.value
        self.how_many = how_many
        self.mod_content = modded

        self._init_production_chain_graph()
        self.product_chains = self.graph.paths_to_root

    def _init_production_chain_graph(self) -> Graph:
        """
        Builds a Production chain graph for a given recipe
        """
        self.graph = Graph(
            root=ComponentNode(
                _try_for_modded_component(self.mod_content, self.name),
                parent_recipe_needs=self.how_many,
                mod_content=self.mod_content,
            ),
            recipe_tree=load_recipes(),
        )

    def build_chain_outputs(self, chain):
        """
        Outputs chains and their total costs
        """

    def build_production_chains(self) -> List[str]:
        """
        Returns a list of all production chains as strings. WARNING VERY LARGE in complex parts
        """

        all_chains = [
            self._string_for_single_chain(chain) for chain in self.graph.paths_to_root
        ]
        all_chains.sort()
        return [f"{i+1}: {chain}" for i, chain in enumerate(all_chains)]

    def _string_for_single_chain(
        self, chain: List[Union[RecipeNode, ComponentNode]]
    ) -> str:
        """
        takes a single chain from self.graph.all_paths_to_root and converts it to a string of recipes.
        """
        chain.reverse()
        return " > ".join(
            [
                node.name.split(":")[1].strip()
                for node in chain
                if isinstance(node, RecipeNode)
            ]
        )

    def __str__(self) -> str:
        return str(self.graph.root)[4:] + "\n"


def check_if_needs_update(component: ComponentName) -> bool:
    """
    Checks if the file has a different last_generated date than the recipes file.
    """
