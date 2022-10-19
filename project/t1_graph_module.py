from typing import Tuple, NamedTuple
import networkx as nx
from cfpq_data import *


class GraphInfo(NamedTuple):
    """Stores information about the number of nodes, edges, and various labels."""

    nodes: int
    edges: int
    labels: set


def create_graph(
    nodes_first: int, nodes_second: int, labels: Tuple[str, str], filepath: str
):
    """Creates a graph with two cycles and labeled edges. After that saves it into DOT file.

    :param nodes_first : Union[int, Iterable[Any]]
        The number of nodes in the first cycle.

    :param nodes_second : Union[int, Iterable[Any]]
        The number of nodes in the second cycle.

    :param labels : Tuple[str, str]
        Labels that will be used to mark the edges of the graph.

    :param filepath : str
        Path to file.
    """
    graph = labeled_two_cycles_graph(nodes_first, nodes_second, labels=labels)
    dot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    dot_graph.write_raw(filepath)


def get_graph_by_name(name: str) -> nx.MultiDiGraph:
    """Loads graph and returns it.

    :param name : str
        Name of the file.

    :raise FileNotFoundError
        If graph with this name doesn't exist

    :return g : MultiDiGraph
        Loaded graph.
    """
    path_to_graph = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path_to_graph)


def get_graph_info(name: str):
    """Loads graph and returns it.

    :param name : str
        Name of the file.

    :return g : GraphInfo
        Actual information about graph.
    """
    graph = get_graph_by_name(name)
    labels = set()
    graph
    for edge in graph.edges(data="label"):
        labels.add(edge[2])
    return GraphInfo(graph.number_of_nodes(), graph.number_of_edges(), labels)
