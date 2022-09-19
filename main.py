from ficsit.effeciency import CompareRecipes
import json
from ficsit.com.components import (
    Equipment,
    ManufacturedComponents,
    ProjectAssemblyPart,
    Ingots,
    display_name_mapping,
    endpoints,
)
from ficsit.com.utils import display_name
from ficsit.com.graph_node import Node, Graph
import plotly.graph_objects as go
from dataclasses import dataclass


def build_visual(graph: Graph):

    data = {
        "ids": [node.ID for node in graph.Nodes.values()],
        "labels": [node.display_name for node in graph.Nodes.values()],
        "parents": [node.parent.ID if node.parent is not None else "" for node in graph.Nodes.values()],
        "customdata": [node.as_dict() for node in graph.Nodes.values()],
        "values":  [
            node.needed_for_parent_cycle
            if node.needed_for_parent_cycle < 100
            else node.needed_for_parent_cycle / 100
            for node in graph.Nodes.values()
        ],
        "hovertext": [
            visual_display_components(node.components) if node.components is not None else "" for node in graph.Nodes.values()
        ],
        "root_color": "lightgrey",
        "tiling": {
            "orientation":"h"
        },
        "textposition": "middle left",
        "count": "leaves"
    }

    fig = go.Figure(go.Icicle(arg=data))

    fig.update_layout(title_text=graph.Root.display_name, font_size=10, margin = dict(t=50, l=25, r=25, b=25))
    fig.show()

    return graph


def visual_display_components(components:dict):
    """
    creates a string that is human eye pleasing for components
    """
    return "Uses:<br \>" + "<br \>".join([f"{value if value < 1000 else value/100} {display_name(key)}" for key,value in components.items()])
        

def main(recipe_name):
    display_name = display_name_mapping.get(recipe_name, recipe_name)

    print(f"Creating document for {display_name}"),
    setup_class = CompareRecipes(recipe_name)

    setup_class.build_all_alternates()

    graph = build_visual(setup_class.graph)
    recipe_paths = setup_class.build_display_paths()
    total_paths = len(recipe_paths)

    output = {"item": display_name, "totalPaths": total_paths, "allPaths": recipe_paths}

    filename = display_name.lower().replace(" ", "_")

    with open(f"./ficsit/possible_paths/{filename}.json", "w") as json_file:
        json.dump(output, json_file, indent=4)

    print(f"... saved with {total_paths} possible paths")

    del setup_class


if __name__ == "__main__":

    for key in display_name_mapping:
        if key not in endpoints:
            main(key)
