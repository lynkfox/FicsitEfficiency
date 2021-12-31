import json

def load_recipes():
    with open("./ficsit/recipes/recipes.json") as file:
        return json.load(file)