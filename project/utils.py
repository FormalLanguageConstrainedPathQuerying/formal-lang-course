import cfpq_data
import networkx
import pathlib
from typing import Dict


def get_graph_info(name: str) -> Dict[str, int]:
    graph = cfpq_data.graph_from_csv(cfpq_data.download(name))
    return {
        "number_of_nodes": graph.number_of_nodes(),
        "number_of_edges": graph.number_of_edges(),
        "unique_labels": set(map(lambda edge: edge[2], graph.edges(data="label"))),
    }


def create_two_cycles_graph(
    nodes_numbers: (int, int), labels: (str, str), path: pathlib.Path
) -> None:

    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_numbers[0], nodes_numbers[1], labels=labels
    )

    networkx.drawing.nx_pydot.write_dot(graph, path)
