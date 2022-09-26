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
        "parents": [
            node.parent.ID if node.parent is not None else ""
            for node in graph.Nodes.values()
        ],
        "values": [
            node.needed_for_parent_cycle
            if node.needed_for_parent_cycle < 100
            else node.needed_for_parent_cycle / 100
            for node in graph.Nodes.values()
        ],
        "text": [extract_display_info_from_node(node) for node in graph.Nodes.values()],
        "root_color": "lightgrey",
        "tiling": {"orientation": "h"},
        "textposition": "top left",
        "count": "leaves",
        "textinfo": "text",
        "hoverinfo": "text",
    }

    data["values"][0] = 1

    fig = go.Figure(go.Icicle(arg=data))

    fig.update_layout(
        title_text=graph.Root.display_name,
        uniformtext={"minsize": 10, "mode": "hide"},
        margin=dict(t=50, l=25, r=25, b=25),
    )
    fig.show()

    return graph


def extract_display_info_from_node(node: Node):
    """
    creates a string that is human eye pleasing for displaying the text on the graph
    """
    full_display = []
    components_list = (
        node.base_components_per_minute_totals
        if node.base_components_per_minute_totals is not None
        else None
    )

    if components_list is None or len(components_list) == 0:
        return node.display_name + "<br \>Base Component"

    for point in components_list:
        format_base_components_values(full_display, point)

    base_values = format_node_basics(node)

    return (
        base_values
        + "<br \><br \>Base Components/min of:<br \>### "
        + "<br \>### ".join(full_display)
    )


def format_node_basics(node: Node) -> str:

    components = [
        f" - {value}/min of {display_name(key)}"
        for key, value in node.components_per_minute.items()
    ]

    return (
        f"{node.display_name}"
        + "<br \># Recipe Per Minute:<br \>"
        + "<br \>".join(components)
    )


def format_base_components_values(full_display: list, point: dict):
    """
    Formats a component and adds it to the list (that is updated by reference)
    """
    component_display = []
    if "Path" in point.keys():
        component_display.append(point["Path"])

    component_display.extend(
        [
            f"  -- {value if value < 1000 else value/100}/min {display_name(key)}"
            for key, value in point.items()
            if value is not None and key != "Path"
        ]
    )
    full_display.append("<br \>".join(component_display))


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
    main(ManufacturedComponents.MODULAR_FRAME)

    # for key in display_name_mapping:
    #     if key not in endpoints:
    #         main(key)
