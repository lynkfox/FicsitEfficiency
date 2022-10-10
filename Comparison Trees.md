# Comparison Trees
#### Comparing alternate paths for the same item

These trees are on a per item base, in what is basically a Directed Action Graph - A root Product in question (produced at 1/min) has Recipes as children, one child for the root node for each recipe that can produce the item.

Each recipe lists its necessary ingredients (and the amount needed to produce the item for the 1/min of the *root item*)

This continues for every item and all its possible recipes all the way down to the basics (Ores, Oil, Water, ect)

## Reading the output:

```
Item (x/min)
  # Recipe for Item
  # Another Recipe for Item
      | Quick Reference to Another Recipe:
         - Ingredient1 for Another Recipe (per min to produce x/min)
         - Ingredient2 for Another Recipe (per min to produce x/min)
         - Power to produce x/min
         * Number buildings to produce x/min
         * square footage of those buildings
         * how many steps down the production chain this is
         ++ Output
         !+ Other Products
      |- Ingredient 1
         # Recipe for Ingredient 1
         # Alternate for Ingredient 1
      |- Ingredient 2
         ....
         and so on until only basic resources remain.
```

if reading the output in visual studio code, it is tabbed and therefor can be collapsed. Some other text reading programs can do this as well.

If you want to compare recipes to each other, the best way to do so is to pick a chain (path from Root (top) all the way to a Leaf (last node of only basic ingredients)) and then look at the very last nodes Input/Output reference. The `-` values listed there will be what is needed to produce that leg of the chain. Pick a chain of recipes for every ingredient for the root  recipe your are comparing and you have everything you'd need
