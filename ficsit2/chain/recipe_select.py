from typing import List, Tuple


def get_possible_recipes(component_name: str, all_recipes: dict) -> List[str]:
    """returns a list of the recipe names"""

    return [recipe["recipeName"] for recipe in all_recipes[component_name]]


def find_recipe_by_name(recipes: List[dict], name: str) -> dict:
    """returns the recipe json by searching for the one with the same name"""
    try:
        return [recipe for recipe in recipes if name in recipe["recipeName"]][0]
    except Exception:
        all_recipes = [recipe for recipe in recipes]
        recipe_names = [recipe["recipeName"] for recipe in all_recipes]
        print(
            f"\n\033[91mCannot find recipe {name}!!!\033[0m defaulting to first recipe in list\n"
            + f"\tAll recipes:\n\t  -"
            + "\n\t  -".join(recipe_names)
            + f"\nUsed: \033[91m{str(recipe_names[0])}\033[0m\n"
        )
        return all_recipes[0]


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
