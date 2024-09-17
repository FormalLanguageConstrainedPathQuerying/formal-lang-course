import cfpq_data
import networkx as nx

from typing import Tuple, Set
from dataclasses import dataclass


@dataclass
class Graph:
    nodes: int  # The number of nodes.
    edges: int  # The number of edges.
    labels: Set[str]  # Edge labels.


def graph_load(graph_name: str) -> nx.MultiDiGraph:
    graph_path = cfpq_data.download(graph_name)  # Getting the path to the graph.
    graph = cfpq_data.graph_from_csv(graph_path)  # Getting the graph itself.

    return graph


def graph_init(graph_name: str) -> Graph:
    graph = graph_load(graph_name)  # Loading the graph.

    nodes = graph.number_of_nodes()  # Getting the number of nodes in the graph.
    edges = graph.number_of_edges()  # Getting the number of edges in the graph.
    labels = set(cfpq_data.get_sorted_labels(graph))  # Getting the labels of edge.

    return Graph(
        nodes,
        edges,
        labels,
    )


def graph_execute(  # Executing a graph.
    first_cycle_nodes: int,
    second_cycle_nodes: int,
    labels: Tuple[str, str],
    path_save: str = "",
) -> nx.MultiDiGraph:  # Creating a graph.
    graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes, second_cycle_nodes, labels=labels
    )

    if path_save:
        graph_save(graph, path_save)  # Saving the graph.

    return graph


def graph_save(graph: nx.MultiDiGraph, path_dot: str) -> None:
    nx.nx_pydot.write_dot(graph, path_dot)  # Saving the graph in DOT format.
