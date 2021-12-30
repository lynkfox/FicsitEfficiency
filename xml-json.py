import json
from xml.etree import ElementTree

def load_xml():
    with open("./recipes/RecipeTable.xml") as file:
        xml = ElementTree.parse(file)

    return xml


def get_recipes(xml_tree):

    all_buildables = xml_tree.findall(".//Recipe")

    all_recipies = {}

    for buildable in all_buildables:
        name = buildable.find("DisplayName")

        if name is None:
            continue

        recipe = get_recipe_details(buildable, name.text)

        if recipe is None:
            continue

        component_produced = buildable.find("Products/ItemAmount").attrib["item"]

        if component_produced in all_recipies:
            all_recipies[component_produced].append(recipe)

        else:
            entry = {
                component_produced: [ recipe ]
            }

            all_recipies.update(entry)


        
    return all_recipies

def get_recipe_details(buildable, name):

    produced_in = buildable.findall(".//ProducedIn/string")

    MACHINES = ["Smelter", "Foundry", "Constructor", "Assembler", "Manufacturer", "OilRefinery", "Blender", "Packager", "HadronCollider"]

    machine = None

    for source in produced_in:
        producers = source.text.split("/")
        producer = producers[-2].replace("Mk1", "") if len(producers) > 2 else None
        if producer not in MACHINES:
            continue
        else:
            if producer == "HadronCollider":
                machine = "ParticleAccelerator"
            else:
                machine = producer
        
    
    if machine is None:
        return None


    return {
        "recipieName": name,
        "producedIn": machine,
        "components": { ingredient.attrib['item']:ingredient.attrib['amount'] for ingredient in buildable.findall(".//Ingredients/ItemAmount")},
        "timeToProduce": int(buildable.find("ManufactoringDuration").text),
        "manualMultiplier": float(buildable.find("ManualManufacturingMultiplier").text)
    }



def main():
    xml = load_xml()

    recipies = get_recipes(xml)

    with open("recipies.json", "w") as json_file:
        json.dump(recipies, json_file)


if __name__ == "__main__":

    main()
