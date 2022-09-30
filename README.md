# FicsitEfficiency

A set of scripts and graphs for comparing any possible permutation of recipes (standard, alternates, and potentially modded) for any component in the game Satisfactory by Coffee Stain Studios

All data about in game assets is Copyright CSS;

## build_recipes.py

One time script run to generate the `.ficsit/data/recipes.json`. Automatically adds the `additional_recipes.json` (U6 updated recipes as the xml is out of date) as well, and if passed `--m` or `--modded` will (todo) include files in the `.ficsit/data/recipes.json` if they are properly formatted (todo)

* e.g.: `python3 build_recipes.py` or `python3 build_recipes.py -m`

## build_graph.py

Creates a graph for a given recipe. See `.ficsit/com/names.py` for the names (under `ComponentName`) - use the human readable display name - and pass with `-c` or `--component` parameter

* e.g.: `python3 build_recipes.py -c "Heavy Modular Frame"`

Will print out the output.

* (Todo) - Visual graph
* (Todo) - Add power, footprint, machines to product chain
* (Todo) - Show totals for each product chain
* (Todo) - Select Recipe Chains to compare (reducing output)
* (Todo) - Select value (Power, Footprint, total Machines, total steps, total raw materials) and have it return product chain that is the best in this value.

## ./ficsit2

main module


## Adding Modded Content

Currently only supporting modded content that is only using Vanilla components(items).

* (todo) write up json schema for recipes
* (todo) add support for adding modded components(items)
