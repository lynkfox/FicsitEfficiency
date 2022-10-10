from dataclasses import dataclass, field
from ficsit2.com.names import ComponentName
from ficsit2.com.node import RecipeNode, ComponentNode, RecipeJson
from ficsit2.com.recipe import TotalProductionValues
from ficsit2.chain.recipe_select import (
    find_recipe_by_name,
    user_pick_recipe,
)
from ficsit2.mod_input.mod_include import ModdedContent
from typing import Dict, List, Tuple


@dataclass
class ChainGraph:

    initial_component: ComponentName
    all_recipes: dict
    produce: float = field(default=1.0)
    recipes_selected: Dict[int, Dict[str, str]] = field(default_factory=dict)
    use_standard: bool = field(default=False)
    mod_content: ModdedContent = field(default=None)
    root: ComponentNode = field(init=False, default=None)
    all_leafs: List[ComponentNode] = field(init=False, default_factory=list)
    total_values: TotalProductionValues = field(init=False)
    final_recipes: List[Tuple[ComponentName, str]] = field(
        init=False, default_factory=list
    )

    def __post_init__(self):
        self.total_values = TotalProductionValues()

        self.root = ComponentNode(
            self.initial_component,
            self.produce,
            parent_cycles_per_minute=self.produce,
            mod_content=self.mod_content,
        )
        self.add_selected_recipe(self.root)
        self.add_selected_component_recipes(self.root.node_children[0].node_children)

        self._generate_total_comparison_values(self.root)

        self.final_recipes.sort(key=lambda x: (x[0].value, x[2]), reverse=True)

    def add_selected_component_recipes(self, components: List[ComponentNode]):
        """
        Iterates through each component child of the recipe passed in, finds the selected recipes for that component
        from the init, and adds a child recipe node to that component
        """
        for component in components:
            if component.node_is_leaf:
                self.all_leafs.append(component)
                continue

            self.add_selected_recipe(component)
            self.add_selected_component_recipes(
                component.node_children[0].node_children
            )

    def add_selected_recipe(self, component: ComponentNode):
        """Finds the correct recipe at the depth of the ComponentNode for the Component and adds that recipe child node"""

        recipe = self._get_recipe(component)

        child_recipe = RecipeNode(
            **RecipeJson(
                **{
                    **recipe,
                    **{"mod_content": self.mod_content, "product": component.name},
                }
            ).props(),
            node_parent=component,
            node_depth=component.node_depth + 1,
        )
        component.node_children.append(child_recipe)
        self.final_recipes.append(
            (component.name, child_recipe.name, component.node_depth)
        )

    def save_recipes(self) -> dict:
        """
        returns a dictionary output of all selected recipes to be saved for future use.
        """
        output = {}
        for recipe_info in self.final_recipes:

            recipe_name = recipe_info[1]
            depth = recipe_info[2]
            component = recipe_info[0].value

            if depth not in output.keys():
                output[depth] = {component: recipe_name}
            else:
                output[depth][component] = recipe_name

        return output

    def _get_recipe(self, component: ComponentNode) -> dict:
        """
        Returns the dictionary of the recipe from the provided recipes. If none is found for a given component, then
        it prompts for input
        """
        recipe = None
        if self.use_standard:
            return find_recipe_by_name(
                self.all_recipes[component.name.value], "Standard"
            )

        if str(component.node_depth) in self.recipes_selected.keys():
            recipe = self.recipes_selected[str(component.node_depth)].get(
                component.name.value
            )

        if recipe is None:
            for component_name, recipe_name, _ in self.final_recipes:
                if component.name == component_name:
                    return find_recipe_by_name(
                        self.all_recipes[component.name.value], recipe_name
                    )

            recipe, self.use_standard = user_pick_recipe(
                component.name.value, self.all_recipes
            )
            return recipe

        if isinstance(recipe, str):
            return find_recipe_by_name(self.all_recipes[component.name.value], recipe)

    def _generate_total_comparison_values(self, component_node: ComponentNode = None):
        """
        returns the entire tree's total comparison values in terms of power, machines, square foot, and total raw materials
        """

        if component_node.node_is_leaf:
            return

        for recipe in component_node.node_children:
            self._add_steps_values(recipe)

            for component in recipe.node_children:
                self._generate_total_comparison_values(component)

    def str_comparison(self):

        all_recipes_needed = list(
            set(
                [
                    f'\t"\033[4m{selection[1]}\033[0m" for {selection[0].value}'
                    for selection in self.final_recipes
                ]
            )
        )
        return (
            f"\n\033[4m\033[92m{self.root.name.value}\033[0m ({self.produce}/min) takes:\n"
            + f"  (using \033[1m{self.root.node_children[0].name}\033[0m)\n\n"
            + str(self.total_values)
            + f"\t  (Producing \033[92m{len(all_recipes_needed)}\033[0m different items)"
            + f"\n\n\033[96mMaking use of:\033[0m\n"
            + f"\n".join(all_recipes_needed)
        )

    def _add_steps_values(self, recipe: RecipeNode):
        self.total_values.add_chain_step(recipe.production_chain_costs)

    def __str__(self) -> str:
        return str(self.root)[4:] + "\n"
