from typing import List, Tuple


def convert_user_dict_to_recipes(all_recipes: dict, initial_picks: dict) -> dict:
    """
    Takes a dict of {node_depth: {component_name: recipe_name} } and converts it to the recipes itself.
    if it cant find a recipe it defaults to the standard one.
    """
    picked_recipes = {}
    for depth, component_set in initial_picks.items():
        picked_recipes[depth] = {}
        for component, recipe_name in component_set.items():
            recipe = all_recipes[component].get(recipe_name)
            if recipe is None:
                recipe = [
                    recipe
                    for recipe in all_recipes[component]
                    if "Standard" in recipe["name"]
                ][0]

            picked_recipes[depth][component if depth > 0 else "root"] = recipe

    return picked_recipes


def get_possible_recipes(component_name: str, all_recipes: dict) -> List[str]:
    """returns a list of the recipe names"""

    return [recipe["recipeName"] for recipe in all_recipes[component_name]]


def find_recipe_by_name(recipes: List[dict], name: str) -> dict:
    """returns the recipe json by searching for the one with the same name"""

    return [recipe for recipe in recipes if name in recipe["recipeName"]][0]


def user_pick_recipe(component_name: str, all_recipes: dict) -> Tuple[dict, bool]:
    """
    Prompts a user for input to select recipes.

    returns a Tuple, of the recipe json, and a bool. If the boolean is True, this is an indicator
    the user wishes to automatically select all future recipes as the Standard variant
    """
    possible_recipes = get_possible_recipes(component_name, all_recipes)

    if len(possible_recipes) == 1:
        return (
            find_recipe_by_name(all_recipes[component_name], possible_recipes[0]),
            False,
        )

    selector = user_recipe_selection_menu(component_name, possible_recipes)

    if selector == len(possible_recipes) + 1:
        return find_recipe_by_name(all_recipes[component_name], "Standard"), True

    else:
        recipe_name = possible_recipes[selector - 1]
        return find_recipe_by_name(all_recipes[component_name], recipe_name), False


def user_recipe_selection_menu(component_name, possible_recipes):
    print(f"\n\033[93mRecipe needed for {component_name}\033[0m\n")
    for i, recipe_name in enumerate(possible_recipes):
        print(f"\t\033[1m{i+1}:\033[0m {recipe_name}")

    print(
        f"\t\033[1m{len(possible_recipes)+1}:\033[0m \033[94mSelect STANDARD variant for this and all other recipes to be selected\033[0m"
    )

    selector = 0
    while selector < 1 or selector > len(possible_recipes) + 1:
        try:
            selector = int(input("\033[4mPlease select an option:\033[0m "))
        except Exception:
            selector = 0

    return selector
