from ficsit.effeciency import CompareRecipes
import json
from ficsit.components import (
    Equipment,
    ManufacturedComponents,
    ProjectAssemblyPart,
    Ingots,
    display_name_mapping,
    endpoints,
)
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

def build_dag(recipe_graph: CompareRecipes):
    graph = nx.DiGraph()
    labels = {}
    edge_labels = {}
    for node in recipe_graph.graph.Nodes.values():
        graph.add_node(node.ID, subset=-node.depth)
        labels[node.ID] = "\n".join(node.display_name.split(" "))
        edge_labels[node.ID] = node.parent_component
        

    for node in recipe_graph.graph.Nodes.values():
        if node.parent is not None:
            graph.add_edge(node.parent.ID, node.ID)
    
    options = {
        "node_size": 3000,
        "node_color": "white",
        "linewidths": 5,
    }
    nx.draw_networkx_labels(graph, pos= nx.drawing.layout.multipartite_layout(graph, align='horizontal'), font_size=6, labels=labels)
    nx.draw_networkx_nodes(graph, pos= nx.drawing.layout.multipartite_layout(graph, align='horizontal'), **options)
    nx.draw_networkx_edges(graph, pos= nx.drawing.layout.multipartite_layout(graph, align='horizontal'))
    ax = plt.gca()
    ax.margins(tight=None)
    plt.axis("off")
    plt.show()

    return graph



def main(recipe_name):
    display_name = display_name_mapping.get(recipe_name, recipe_name)

    print(f"Creating document for {display_name}"),
    setup_class = CompareRecipes(recipe_name)

    setup_class.build_all_alternates()

    graph = build_dag(setup_class)
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
