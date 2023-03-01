from collections import namedtuple

import networkx as nx
import cfpq_data as cd


def load_graph(name):
    return cd.graph_from_csv(cd.download(name))


def save_graph(graph: nx.MultiDiGraph, filename):
    nx.drawing.nx_pydot.write_dot(graph, filename)


def get_vertices_number(graph: nx.MultiGraph):
    return graph.number_of_nodes()


def get_edges_number(graph: nx.MultiGraph):
    return graph.number_of_edges()


def get_edges_labels(graph: nx.MultiGraph):
    return set(label for _, _, label in graph.edges(data="label") if label)


def get_graph_info(graph: nx.MultiGraph):
    graph_info = namedtuple("graph_info", ["num_vertices", "num_edges", "edges_labels"])
    return graph_info(
        get_vertices_number(graph), get_edges_labels(graph), get_edges_labels(graph)
    )


def build_two_cycle_graph(first_cycle, second_cycle, labels):
    return cd.labeled_two_cycles_graph(first_cycle, second_cycle, labels=labels)


def build_and_save_two_cycle_graph(first_cycle, second_cycle, labels, path):
    graph = build_two_cycle_graph(first_cycle, second_cycle, labels)
    save_graph(graph, path)
    return graph
