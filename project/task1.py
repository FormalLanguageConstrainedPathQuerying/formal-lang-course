from pathlib import Path
from typing import Set, Tuple

import cfpq_data
from networkx import Graph, MultiDiGraph
from networkx.drawing.nx_pydot import write_dot

__all__ = [
    "GraphData",
    "get_graph_data",
    "write_labeled_two_cycles_graph_to_dot",
]


class GraphData:
    """Graph data including number of node, number of edges, and set of
    labels"""

    node_count: int
    edge_count: int

    labels: Set[str]
    """The set of values of the "label" attribute of graph edges"""

    def __init__(self, node_count: int, edge_count: int, labels: Set[str]):
        self.node_count = node_count
        self.edge_count = edge_count
        self.labels = labels

    def __eq__(self, other):
        return (
            isinstance(other, GraphData)
            and self.node_count == other.node_count
            and self.edge_count == other.edge_count
            and self.labels == other.labels
        )

    def __repr__(self):
        return (
            f"GraphData(node_count={self.node_count}, "
            f"edge_count={self.edge_count}, "
            f"labels={self.labels})"
        )


def get_graph_data(graph_name: str) -> GraphData:
    return _to_graph_data(_get_graph(graph_name))


def _get_graph(graph_name: str) -> MultiDiGraph:
    graph_path = cfpq_data.download(graph_name)
    return cfpq_data.graph_from_csv(graph_path)


def _to_graph_data(graph: Graph) -> GraphData:
    return GraphData(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set(attributes["label"] for (_, _, attributes) in graph.edges.data()),
    )


def write_labeled_two_cycles_graph_to_dot(
    cycle_sizes: Tuple[int, int], labels: Tuple[str, str], path: Path
):
    """
    Writes a graph with two cycles connected by one node two a dot file

    :param cycle_sizes: The number of nodes in cycles without a common node
    :param labels: Labels that will be used to mark the edges of the graph
    :param path: Filepath to write graph to
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        n=cycle_sizes[0], m=cycle_sizes[1], labels=labels
    )
    write_dot(graph, path)
