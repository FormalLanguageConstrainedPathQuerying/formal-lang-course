import os

import networkx
from cfpq_data import *
from scripts import shared


class Graph:
    """
    A class with information about the number of vertices, edges, and graph labels.
    """

    def __init__(self, number_of_nodes, number_of_edges, labels):
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.labels = labels


def get_labels(edges):
    """
    Gets labels on edges and returns set.
    :param edges:
    :return: set (labels)
    """
    return set(map(lambda node: node[2]["label"], edges.data()))


def get_info_by_graph(graph):
    """
    Returns information about the graph object.
    :param graph: MultiDiGraph()
    :return: Graph()
    """
    return Graph(
        graph.number_of_nodes(), graph.number_of_edges(), get_labels(graph.edges)
    )


def get_info_by_name(graph_name):
    """
    Returns information about the graph name.
    :param graph_name: str
    :return: Graph()
    """
    path_to_graph = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path_to_graph)
    return Graph(
        graph.number_of_nodes(), graph.number_of_edges(), get_labels(graph.edges)
    )


def create_two_cycles_graph(nodes_in_first_cycle, nodes_in_sec_cycle, labels):
    """
    Creates a graph of two cycles.
    :param nodes_in_first_cycle: int
    :param nodes_in_sec_cycle: int
    :param labels: Tuple[,]
    :return: MultiDiGraph ()
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_in_first_cycle, nodes_in_sec_cycle, labels=labels
    )
    return graph


def save_in_dot(graph_networkx):
    """
    Saves the graph to a file in dot format.
    :param graph_networkx: MultiDiGraph ()
    """
    networkx.drawing.nx_pydot.write_dot(
        graph_networkx, str(shared.ROOT) + os.sep + "output" + os.sep + "graph.dot"
    )
