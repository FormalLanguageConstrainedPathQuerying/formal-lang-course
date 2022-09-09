import cfpq_data

from typing import IO
from networkx import drawing, MultiDiGraph
from collections import namedtuple
from pathlib import Path

GraphInfo = namedtuple("GraphInfo", "nodes_num edges_num labels")
"""
Namedtuple of number of nodes, number of edges, set of edges' labels.
"""


def get_graph(name: str) -> MultiDiGraph:
    """
    Finds graph with a given name.

    :param name: Name of graph to find.
    :return: Existing graph with a given name from CFPQ_Data Dataset.
    :raises FileNotFoundError: if no graph with given name found.
    """
    graph_path = cfpq_data.dataset.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)

    return graph


def get_graph_info(name: str) -> GraphInfo:
    """
    Show basic info of a graph with a given name from CFPQ_Data Dataset.

    :param name: Name of graph to find.
    :return: Namedtuple of number of nodes, number of edges, set of edges' labels.
    :raises FileNotFoundError: if no graph with given name found.
    """
    graph = get_graph(name)
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {i[2]["label"] for i in graph.edges.data(default=True)},
    )


def generate_labeled_two_cycles_graph(
    nodes_num: tuple[int, int],
    labels: tuple[str, str],
) -> MultiDiGraph:
    """
    Returns a graph with two cycles with labeled edges.

    :param nodes_num: Numbers of nodes in two cycles.
    :param labels: Labels for edges in two cycles.
    :return: A graph with two cycles connected by one node.
    """
    return cfpq_data.labeled_two_cycles_graph(
        nodes_num[0],
        nodes_num[1],
        labels=labels,
    )


def export_graph_to_dot(graph: MultiDiGraph, path: str | IO) -> Path:
    """
    Exports the given graph into the specified DOT file.

    :param graph: Graph to export.
    :param path: Path to dot file.
    :return: Path to file.
    """
    dot = drawing.nx_pydot.to_pydot(graph)
    dot.write_raw(path)

    return Path(path)
