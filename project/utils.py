import cfpq_data
import networkx as nx

from dataclasses import dataclass
from typing import Set, Tuple


@dataclass
class Graph:
    node_count: int
    edge_count: int
    edge_labels: Set[str]


def load_graph(graph_name: str) -> nx.MultiDiGraph:
    path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path)

    return graph


def get_graph(graph_name: str) -> Graph:
    graph = load_graph(graph_name)

    return Graph(
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        edge_labels=set(cfpq_data.get_sorted_labels(graph)),
    )


def create_labeled_two_cycles_graph(
    first_cycle_node_count: int,
    second_cycle_node_count: int,
    labels: Tuple[str, str],
    save_path: str = "",
) -> nx.MultiDiGraph:
    graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_node_count, second_cycle_node_count, labels=labels
    )
    if save_path:
        save_graph_to_dot(graph, save_path)

    return graph


def save_graph_to_dot(graph: nx.MultiDiGraph, dot_path: str) -> None:
    nx.nx_pydot.write_dot(graph, dot_path)
