from typing import Set

import cfpq_data
import networkx


class GraphInformation:
    """
    
    """
    nodes: int
    edges: int
    labels: Set[str]

    def __init__(self, nodes, edges, labels):
        self.nodes = nodes
        self.edges = edges
        self.labels = labels

    def __eq__(self, other):
        result = (
                isinstance(other, GraphInformation)
                and self.nodes == other.nodes
                and self.edges == other.edges
                and self.labels == other.labels
        )

        return result


def get_graph_info(graph_name):
    """

    """
    path = cfpq_data.download(graph_name)

    graph = cfpq_data.graph_from_csv(path)
    # TODO: add documentation!!!

    nodes_num = graph.number_of_nodes()
    edges_num = graph.number_of_edges()
    labels = set(cfpq_data.get_sorted_labels(graph))

    return GraphInformation(nodes_num, edges_num, labels)


def generate_and_write_two_cycles_graph(num_first, num_second, labels, path):
    """

    """
    graph = cfpq_data.labeled_two_cycles_graph(num_first, num_second, labels=labels)

    networkx.nx_pydot.write_dot(graph, path)
