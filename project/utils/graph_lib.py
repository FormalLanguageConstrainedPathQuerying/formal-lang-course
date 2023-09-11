import cfpq_data
import networkx as nx
from typing import Tuple


def create_two_cycle_graph(
    first_count_nodes: int, second_count_nodes: int, labels: Tuple[str, str], path: str
) -> None:
    """
    Creates a two cycle graph using the given numbers of vertices in two cycles, pairs of labels and saves it to a
    file at a given path

    Parameters
    ----------
    first_count_nodes: int
    number of nodes in the first cycle
    second_count_nodes: int
    number of nodes in the second cycle
    labels: Tuple[str, str]
    A pair of labels for the graph
    path: str
    A given path containing the file name, both with and without the .dot extension
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        first_count_nodes, second_count_nodes, labels=labels
    )
    pydot_graph = nx.nx_pydot.to_pydot(graph)
    if not path.endswith(".dot"):
        path = path + ".dot"
    with open(path, "w") as file:
        file.write(pydot_graph.to_string().replace("\n", ""))


def get_graph_by_name(graph_name: str) -> (int, int, set):
    """
    Given a graph name, loads a graph from the dataset and returns the number of nodes, edges and set of graph labels

    Parameters
    ----------
    graph_name: str
    Name of graph

    Returns
    -------
    nodes, edges, labels: (int, int, set)
    The number of nodes, edges and set of graph labels

    Raises
    ----------
    FileNotFoundError
    If there is no graph with a given name in the dataset
    """
    try:
        path_to_graph = cfpq_data.download(graph_name)
        graph = cfpq_data.graph_from_csv(path_to_graph)
        return (
            graph.number_of_nodes(),
            graph.number_of_edges(),
            set(d["label"] for _, _, d in graph.edges(data=True)),
        )
    except FileNotFoundError as e:
        raise e
