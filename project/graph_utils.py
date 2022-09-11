from typing import NamedTuple
import cfpq_data
import networkx as nx

__all__ = [
    "Graph",
    "get_graph_info",
    "get_graph",
    "create_two_cycles_graph_and_save_as_dot",
]


class Graph(NamedTuple):
    """Class that contains the number of vertices, the number of edges, and the set of labels on the edges in the
    graph."""

    nodes: int
    edges: int
    labels: set


def get_graph_info(name) -> Graph:
    """Get information about a graph by name.

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Returns
    -------
    graph : Graph
        The class containing information about a graph.
    """
    graph = get_graph(name)
    labels = set()
    for (_, _, l) in graph.edges(data="label"):
        labels.add(l)
    return Graph(graph.number_of_nodes(), graph.number_of_edges(), labels)


def get_graph(name) -> nx.MultiDiGraph:
    """Get a graph by name from a dataset.

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Returns
    -------
    graph : MultiDiGraph
        The graph.
    """
    path = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path)


def create_two_cycles_graph_and_save_as_dot(
    cycle_sizes: tuple[int, int], labels: tuple[str, str], file_path
) -> None:
    """Create a labeled two cycles graph and save it to the file in DOT format.

    Parameters
    ----------
    cycle_sizes: tuple[int, int]
        The number of vertices in the first and second cycles.
    labels: tuple[str, str]
        Labels that will be used to mark the edges of the graph.
    file_path: str
        The name or path to the file where the graph should be saved.
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        cycle_sizes[0], cycle_sizes[1], labels=labels
    )
    nx.drawing.nx_pydot.write_dot(graph, file_path)
