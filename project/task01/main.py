import os
from dataclasses import dataclass
from networkx.drawing.nx_pydot import write_dot
from networkx.classes.reportviews import OutMultiEdgeView

import cfpq_data as cfpq


@dataclass
class GraphProperties:
    nodes_count: int
    edges_count: int
    edges: OutMultiEdgeView


def get_graph_properties(name: str) -> GraphProperties:
    """
    :param name:
        The path to the CSV file that contains graph
    :return:
    """
    path = cfpq.download(name)
    graph = cfpq.graph_from_csv(path)  # assert?
    return GraphProperties(
        nodes_count=graph.number_of_nodes(),
        edges_count=graph.number_of_edges(),
        edges=graph.edges(data=True),
    )


def twocycle_to_dot(path: str, n: int, m: int, *, labels=None):
    if labels is None:
        labels = {"first", "second"}
    graph = cfpq.labeled_two_cycles_graph(n, m, labels=labels)
    write_dot(graph, path)
