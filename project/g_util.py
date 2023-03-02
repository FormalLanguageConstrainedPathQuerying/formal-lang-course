from typing import Set

import cfpq_data as cfpq
import networkx as nx


class GraphInformation:
    """
    Class representing information about graph
    """
    def __init__(self, nodes, edges, edges_labels):
        self.nodes = nodes
        self.edges = edges
        self.edges_labels = edges_labels

    def __eq__(self, other):
        return (
                self.nodes == other.nodes
                and self.edges == other.edges
                and self.edges_labels == self.edges_labels
        )


def get_graph_information(graph: nx.MultiDiGraph) -> GraphInformation:
    """
    Gets number of nodes and edges, gets edge labels from a graph
    :param graph: target graph
    :return: GraphInformation
    """
    edge_labels = set(label for _, _, label in graph.edges(data="label") if label)
    return GraphInformation(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        edge_labels,
    )


def build_two_cycle_labeled_graph(first_cycle: int, second_cycle: int, edge_labels: Set) -> nx.MultiDiGraph:
    """
    Builds a graph with two cycles and edge labels
    :param first_cycle: Number of nodes in the first cycle.
    :param second_cycle: Number of nodes in the second cycle.
    :param edge_labels: Edge labels.
    :return: Graph with two cycles connected by one node.
    """
    return cfpq.labeled_two_cycles_graph(n=first_cycle, m=second_cycle, labels=edge_labels)


def load_graph(graph_name: str) -> nx.MultiDiGraph:
    """
    Loads a graph from dataset.
    :param graph_name: Name of the graph.
    :return: Graph
    """
    return cfpq.graph_from_csv(cfpq.download(graph_name))


def save_graph_to_file(graph: nx.MultiDiGraph, file):
    """
    Saves a graph to the file
    :param graph: Graph to save
    :param file: Path that can be a string or a file handle.
    :return: None
    """
    nx.drawing.nx_pydot.write_dot(graph, file)


def read_graph_from_file(file) -> nx.Graph:
    """
    Reads a graph from the file
    :param file: Path that can be a string or a file handle.
    :return: Graph
    """
    return nx.drawing.nx_pydot.read_dot(file)
