import cfpq_data
import networkx as nx

from cfpq_data import get_sorted_labels, labeled_two_cycles_graph
from typing import Tuple


def get_graph(name: str):
    graph_archive = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_archive)  # loading graph by path
    return graph


def graph_data(graph_name: str):
    graph = get_graph(graph_name)

    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    labels = get_sorted_labels(graph)

    return nodes, edges, labels


def create_labeled_two_cycles_graph(
    n: int, m: int, labels: Tuple[str, str], path_to_save: str
):
    graph = labeled_two_cycles_graph(n, m, labels=labels)

    graph_dot = nx.drawing.nx_pydot.to_pydot(graph)
    graph_dot.write(path_to_save)
