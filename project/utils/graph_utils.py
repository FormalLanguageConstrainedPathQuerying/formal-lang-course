from collections import namedtuple
from pathlib import Path
from networkx import MultiDiGraph

import cfpq_data
import networkx as nx

GraphInfo = namedtuple("GraphInfo", ["nodes", "edges", "labels"])


class GraphException(Exception):
    """
    Base exception for graph utils
    """

    def __init__(self, msg):
        self.msg = msg


def get_graph(name: str, env: dict = None) -> MultiDiGraph:
    """
    Finds graph with a given name.
    First search in given environment, then in CFPQ_Data Dataset

    Parameters
    ----------
    name: str
        Name of graph to find
    env : dict, default=None

    Returns
    -------
    g : MultiDiGraph
        Existing graph with a given name
    """
    if not env:
        env = dict()

    if name in env.keys():
        graph = env[name]
    else:
        graph = cfpq_data.graph_from_dataset(name, verbose=False)

    if not graph:
        raise GraphException(f"Graph '{name}' is absent in dataset")

    return graph


def get_graph_info(name: str, env: dict = None) -> GraphInfo:
    """
    Show basic info of a graph with a given name
    First search in env, then in cfpq_data.dataset.DATASET

    Parameters
    ----------
    name : str
        Name of real-world graph from CFPQ_Data Dataset.
    env : dict, default=None

    Returns
    -------
    info : GraphInfo
        Namedtuple of (number of nodes, number of edges, set of edges' labels)
    """

    graph = get_graph(name, env)

    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_two_cycles_graph(
    first_cycle_nodes_num: str,
    second_cycle_nodes_num: str,
    first_cycle_label: str,
    second_cycle_label: str,
) -> MultiDiGraph:
    """
    Returns a graph with two cycles connected by one node.
    With labeled edges.

    Parameters
    ----------
    first_cycle_nodes_num : int
        Number of nodes in the first cycle
    second_cycle_nodes_num : int
        Number of nodes in the second cycle
    first_cycle_label : str
        Labels on the graph's first cycle
    second_cycle_label : str
        Labels on the graph's second cycle

    Returns
    -------
    g : MultiDiGraph
        A graph with two cycles connected by one node.
    """
    if not first_cycle_nodes_num.isdigit():
        raise GraphException(
            f"first_cycle_nodes_num expected to be Int, got {type(first_cycle_nodes_num)} instead"
        )
    if not second_cycle_nodes_num.isdigit():
        raise GraphException(
            f"second_cycle_nodes_num expected to be Int, got {type(second_cycle_nodes_num)} instead"
        )

    return cfpq_data.labeled_two_cycles_graph(
        int(first_cycle_nodes_num),
        int(second_cycle_nodes_num),
        edge_labels=(first_cycle_label, second_cycle_label),
        verbose=False,
    )


def save_to_dot(graph: MultiDiGraph, path_to_file: str):
    """
    Saves graph to given path in DOT format

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save
    path_to_file : str
        Path to file

    Returns
    -------
    p : Path
        Path to file
    """
    g = nx.drawing.nx_pydot.to_pydot(graph)

    g.write_raw(path_to_file)

    return Path(path_to_file)
