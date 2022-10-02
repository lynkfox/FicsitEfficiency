# Adding modded recipes
#### Currently Only Good with Vanilla Parts

* Add a json file to `.input/modded` - call it whatever you want, but no spaces in the name.
* Each recipe needs to follow [recipe_schema](recipe_schema.json)
* Each recipe goes in an Array in a parent dictionary with the key being the name of the Product being produced (which must be at most one entry in recipe_schema.produces)

## Example

`..input/modded/my_mod_recipes.json`

```json
{
    "Coal": [
        {
            "recipeName": "Modded: Carbon Coal",
            "producedIn": "Constructor",
            "producesPerCycle": 30,
            "components": [
                {
                    "name": "Leaves",
                    "amount": 100,
                    "measurement": "items/productionCycle"
                }
            ],
            "cycleTime": 12,
            "products": [
                "Coal"
            ]
        }
    ]
}
```
