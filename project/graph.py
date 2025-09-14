from __future__ import annotations
from typing import Tuple, Set
import cfpq_data
import cfpq_data.graphs.readwrite as rw
import networkx


class Info:
    def __init__(self, number_of_nodes: int, number_of_edges: int, labels: Set[str]):
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.labels = labels

    def from_file(name: str) -> Info:
        g = rw.graph_from_csv(cfpq_data.download(name))
        number_of_edges = g.number_of_edges
        number_of_nodes = g.number_of_nodes
        labels = {g.edges[edge]["label"] for edge in g.edges}
        return Info(number_of_nodes, number_of_edges, labels)


def create_and_safe_2cycle_graph(
    cycle1_number_of_nodes: int,
    cycle2_number_of_nodes: int,
    labels: Tuple[str, str],
    out: str,
) -> None:
    """
    Create a graph with two cycles connected by one node. With labeled edges.
    And save it to a specified file in DOT format.

    cycleX_number_of_nodes doesn't include common node.
    """

    g = cfpq_data.labeled_two_cycles_graph(
        cycle1_number_of_nodes, cycle2_number_of_nodes, labels=labels
    )
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(g)
    pydot_graph.write_raw(out)
