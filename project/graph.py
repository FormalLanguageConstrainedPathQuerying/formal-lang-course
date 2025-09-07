from typing import Tuple, Set
import cfpq_data
import networkx


class Info:
    number_of_nodes = 0
    number_of_edges = 0
    labels: Set[str] = set()

    def __init__(self, name):
        g = cfpq_data.download(name)
        self.number_of_edges = g.number_of_edges
        self.number_of_nodes = g.number_of_nodes
        self.labels = {edge.label for edge in g.edges}


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
