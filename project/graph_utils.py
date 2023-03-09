import cfpq_data
import networkx
from networkx import MultiDiGraph
import pathlib
from typing import Dict


def get_graph_info(name: str) -> Dict[str, int]:
    """
    Return the number of vertices, edges, and edges labels
    from graph by name

    Args:
        name: name of the graph

    Returns:
        dicttionary with number of nodes, edges and its labels
    """
    graph = cfpq_data.graph_from_csv(cfpq_data.download(name))
    return {
        "number_of_nodes": graph.number_of_nodes(),
        "number_of_edges": graph.number_of_edges(),
        "unique_labels": set(map(lambda edge: edge[2], graph.edges(data="label"))),
    }


def create_two_cycles_graph(
    nodes_numbers: (int, int), labels: (str, str), path: pathlib.Path
) -> MultiDiGraph:
    """
    Builds two cycle graph and saves it to a .dot file

    Args:
        nide_numbers: tuple of number of vertices in cycles
        labels: tuple of label names
        path: output file path

    Returns:
        Created graph
    """

    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_numbers[0], nodes_numbers[1], labels=labels
    )

    networkx.drawing.nx_pydot.write_dot(graph, path)

    return graph
