from pathlib import Path

import cfpq_data as cfpq
import networkx as nx


def load_graph(name: str) -> nx.MultiDiGraph:
    """Loads a graph from dataset

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Returns
    -------
    graph : networkx.MultiDiGraph
        Loaded graph.

    """
    path = cfpq.download(name)
    return cfpq.graph_from_csv(path)


def load_graph_info(name: str) -> tuple[int, int, set[str]]:
    """Loads a graph info(number of edges, number of nodes, labels on edges)
     from dataset

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Returns
    -------
    result : tuple[number of edges, number of nodes, set of labels]
        Loaded graph info

    """
    graph = load_graph(name)

    labels = set()
    for _, _, label in graph.edges(data="label", default=None):
        if label is not None:
            labels.add(label)

    return graph.number_of_edges(), graph.number_of_nodes(), labels


def save_graph_as_dot(graph: nx.MultiDiGraph, path: str) -> bool:
    """Loads a graph to a dot file

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        Loadable graph
    path : str
        Filename

    Returns
    -------
    result : bool
        Returns True or False according to the success of the write
        operation.
    """
    fixed_path = Path(path)
    return nx.drawing.nx_pydot.write_dot(graph, fixed_path)


def save_labeled_two_cycles_graph_as_dot(
    n: int, m: int, labels: tuple[str, str], path: str
) -> bool:
    """Create and loads labeled two cycles graph to a dot file

    Parameters
    ----------
    n : int
        The number of nodes in the first cycle without a common node.

    m : int
        The number of nodes in the second cycle without a common node.

    labels: Tuple[str, str]
        Labels that will be used to mark the edges of the graph.

    Returns
    -------
    result : bool
        Returns True or False according to the success of the write
        operation.
    """
    return save_graph_as_dot(cfpq.labeled_two_cycles_graph(n, m, labels=labels), path)
