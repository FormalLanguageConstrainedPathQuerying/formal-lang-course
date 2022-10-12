import cfpq_data
import networkx as nx
from collections import namedtuple
from typing import Tuple

__all__ = [
    "graph_info",
    "get_graph_info",
    "get_graph_info_by_name",
    "create_labeled_two_cycles_graph",
    "save_graph_as_dot",
    "load_graph_from_dot",
    "create_and_save_labeled_two_cycles_graph",
]

graph_info = namedtuple("graph_info", "graph number_of_nodes number_of_edges labels")


def get_graph_info(graph: nx.MultiDiGraph) -> graph_info:
    keys = set(label for _, _, label in graph.edges(data="label") if label)
    return graph_info(graph, graph.number_of_nodes(), graph.number_of_edges(), keys)


def get_graph_info_by_name(graph_name: str) -> graph_info:
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return get_graph_info(graph)


def create_labeled_two_cycles_graph(
    first_cycle_size: int, second_cycle_size: int, labels: Tuple[str, str] = ("a", "b")
) -> nx.MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(
        first_cycle_size, second_cycle_size, labels=labels
    )


def save_graph_as_dot(graph: nx.MultiDiGraph, path: str) -> None:
    nx.drawing.nx_pydot.write_dot(graph, path)


def load_graph_from_dot(path: str) -> nx.MultiDiGraph:
    return nx.drawing.nx_pydot.read_dot(path)


def create_and_save_labeled_two_cycles_graph(
    first_cycle_size: int, second_cycle_size: int, labels: Tuple[str, str], path: str
) -> None:
    save_graph_as_dot(
        create_labeled_two_cycles_graph(first_cycle_size, second_cycle_size, labels),
        path,
    )
