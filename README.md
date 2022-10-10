# FicsitEfficiency

A set of scripts and graphs for comparing any possible permutation of recipes (standard, alternates, and potentially modded) for any component in the game Satisfactory by Coffee Stain Studios

All data about in game assets is Copyright CSS;

## component_compare_values.py

This takes a single item and builds the compare values for a single tree of recipes - that is one recipe per item.

run with: `python3 component_compare_values.py -c "Name of the Component"` - It will ask you what recipe to pick for each stage. By default it will re-use the same recipe selected for a previous similar component: i.e. if the tree of recipes uses Iron Ingots in more than one location, as soon as a recipe for Iron ingots is selected, that will be used for all other locations of Iron Ingots.

* e.g. `python3 component_compare_values.py -c "Heavy Modular Frame"`
* Pass the `-o` flag to use Only *Standard* recipes
  * instead use `-i` to specify a json file name stored in `./output/user/` to pre-selected recipes in.
  * This is mutually exclusive to the `-o` flag and vice versa
  * this is the only way to select different recipes for the same item: ie using the Standard recipe for Iron Ingots underneath RIPs but using the Iron Alloy recipe for Iron Ingots underneath Iron Wire.
  * See `input/schema/select_recipes_schema.json` for more information.
* Pass the `-s` flag to save the output to `output/user/[name_of_component]_[datetimestring].txt`
* Pass the `-r` flag to save a copy of all the recipes used for each component at each depth to `output/user/[name_of_component]_[datetimestring].json`
* Pass the `-f` flag with either/both `-s` or `-r` to specify a suffix for the output, such as `-r -f "all_standard"` which would result in an output of recipes to a file name `output/user/[name_of_component]_all_standard.json`
* Pass `-q` to suppress the output at the end (any missing recipes will be still selected)

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
* (Todo) - Select value (Power, Footprint, total Machines, total steps, total raw materials) and have it return product chain that is the best in this value.

## ./ficsit2

main module


## Adding Modded Content

Currently only supporting modded content that is only using Vanilla components(items).

* (todo) write up json schema for recipes
* (todo) add support for adding modded components(items)
