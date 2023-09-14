from typing import Tuple
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot
import cfpq_data

from project.graph_data import GraphData


def download_graph(name: str) -> MultiDiGraph:
    """
    Downloads the graph from CFPQ dataset by name

    Args:
        name: name of graph in CFPQ dataset

    Returns:
        Graph downloaded
    """
    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return graph


def save_graph(G: MultiDiGraph, path: str) -> None:
    """
    Save graph in the DOT format into the path provided

    Args:
        path: path to be saved to
    """
    with open(path, "w+") as f:
        write_dot(G, f)


def get_graph_data(G: MultiDiGraph) -> GraphData:
    """
    Gets number of nodes, edges and set of different labels of the graph given

    Args:
        G: graph to be analyzed

    Returns:
        Graph data with number of nodes, edges and set of different labels
    """

    def get_label(edge):
        return edge[2]

    labels = set(map(get_label, G.edges(data="label")))
    return GraphData(G.number_of_nodes(), G.number_of_edges(), labels)


def get_graph_data_by_name(name: str) -> GraphData:
    """
    Downloads graph by name from CFPQ dataset, and then
    gets number of nodes, edges and set of different labels of the graph given

    Args:
        name: name of graph in CFPQ dataset to be analyzed

    Returns:
        Graph data with number of nodes, edges and set of different labels
    """
    return get_graph_data(download_graph(name))


def create_labeled_two_cycle_graph(
    n: int, m: int, labels: Tuple[str, str]
) -> MultiDiGraph:
    """
    Creates two cycled graph connected by one node from amount of nodes in cycles and labels

    Args:
        n: amount of nodes in the first cycle without a common node
        m: amount of nodes in the second cycle without a common node
        labels: Labels that will be used to mark the edges of the graph

    Returns:
        A graph with two cycles connected by one node with labeled edges
    """
    return cfpq_data.labeled_two_cycles_graph(n, m, 0, labels)


def create_labeled_two_cycle_graph_and_save(
    n: int, m: int, labels: Tuple[str, str], path: str
) -> None:
    """
    Creates two cycled graph connected by one node from amount of nodes in cycles and labels
    and saves it to the path given

    Args:
        n: amount of nodes in the first cycle without a common node
        m: amount of nodes in the second cycle without a common node
        labels: Labels that will be used to mark the edges of the graph
        path: path to be saved to

    """
    G = create_labeled_two_cycle_graph(n, m, labels)
    save_graph(G, path)
