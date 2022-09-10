import os

import networkx
from cfpq_data import *
from scripts import shared


class Graph:
    def __init__(self, number_of_nodes, number_of_edges, labels):
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.labels = labels


def get_labels(edges):
    return set(map(lambda node: node[2]["label"], edges.data()))


def get_info_by_graph(graph):
    return Graph(
        graph.number_of_nodes(), graph.number_of_edges(), get_labels(graph.edges)
    )


def get_info_by_name(graph_name):
    path_to_graph = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path_to_graph)
    return Graph(
        graph.number_of_nodes(), graph.number_of_edges(), get_labels(graph.edges)
    )


def create_two_cycles_graph(nodes_in_first_cycle, nodes_in_sec_cycle, labels):
    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_in_first_cycle, nodes_in_sec_cycle, labels=labels
    )
    return graph


def save_in_dot(graph_networkx):
    print(str(shared.ROOT))
    networkx.drawing.nx_pydot.write_dot(
        graph_networkx, str(shared.ROOT) + os.sep + "output" + os.sep + "graph.dot"
    )
