import cfpq_data
import networkx.drawing.nx_pydot
from collections import namedtuple

__all__ = [
    "graph_info",
    "get_graph_info",
    "get_graph_info_by_name",
    "create_labeled_two_cycles_graph",
    "save_graph_as_dot",
    "create_and_save_labeled_two_cycles_graph",
]

graph_info = namedtuple("graph_info", "number_of_nodes number_of_edges lables")


def get_graph_info(graph):
    keys = set(label for _, _, label in graph.edges(data="label") if label)
    return graph_info(graph.number_of_nodes(), graph.number_of_edges(), keys)


def get_graph_info_by_name(graph_name):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return get_graph_info(graph)


def create_labeled_two_cycles_graph(
    first_cycle_size, second_cycle_size, lables=("a", "b")
):
    return cfpq_data.labeled_two_cycles_graph(
        first_cycle_size, second_cycle_size, labels=lables
    )


def save_graph_as_dot(graph, path):
    networkx.drawing.nx_pydot.write_dot(graph, path)


def create_and_save_labeled_two_cycles_graph(
    first_cycle_size, second_cycle_size, lables, path
):
    save_graph_as_dot(
        create_labeled_two_cycles_graph(first_cycle_size, second_cycle_size, lables),
        path,
    )
