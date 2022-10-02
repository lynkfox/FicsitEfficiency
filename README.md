# FicsitEfficiency

A set of scripts and graphs for comparing any possible permutation of recipes (standard, alternates, and potentially modded) for any component in the game Satisfactory by Coffee Stain Studios

All data about in game assets is Copyright CSS;

## build_recipes.py

One time script run to generate the `.ficsit/data/recipes.json`. Automatically adds the `additional_recipes.json` (U6 updated recipes as the xml is out of date) as well, and if passed `--m` or `--modded` will (todo) include files in the `.input/modded/*` directory if they are properly formatted (todo)

* e.g.: `python3 build_recipes.py` or `python3 build_recipes.py -m`
* Currently can do modded recipes if they only use vanilla parts.
* See [Modded Recipes Readme](schema/ModdedRecipes.md) for the JSON schema for adding additional recipes

## build_comparison_trees.py.py

Creates a graph for a given recipe. See `.ficsit/com/names.py` for the names (under `ComponentName`) - use the human readable display name

* pass with `-c` or `--component` parameter with the ComponentName from above
  * `python3 build_comparison_trees.py -c "Heavy Modular Frame"`
  * outputs to `.output/recipe_comparison_trees/component_name.txt`
    *  i.e.: `.output/recipe_comparison_trees/heavy_modular_frame.txt`
* can also pass `-p` to determine how many to Produce/per minute
  * `python3 build_comparison_trees.py -c "Heavy Modular Frame" -p 10`
  * If p is anything other than 1, will instead output to `./output/user/component_name.txt` and overwrite any existing file of the same name.
* can also pass `-a` to build ALL the comparison trees (usually takes between 15-20 seconds)
* can pass `-v` up to `-vvv` three times, with the last one outputting the tree into the terminal and NOT building a file
  * really really really bad idea to do `-a -vvv` but thats your systems funeral.

Will print out the output.

* (Todo) - Visual graph
* (Todo) - Show totals for each product chain
* (Todo) - Select Recipe Chains to compare (reducing output)
* (Todo) - Select value (Power, Footprint, total Machines, total steps, total raw materials) and have it return product chain that is the best in this value.

## ./ficsit2

main module


## Adding Modded Content

Currently only supporting modded content that is only using Vanilla components(items).

* (todo) write up json schema for recipes
* (todo) add support for adding modded components(items)
