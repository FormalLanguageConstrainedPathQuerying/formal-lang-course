import cfpq_data
import networkx as nx
from collections import namedtuple

GraphInfo = namedtuple("GraphInfo", ["nodes_count", "edges_count", "labels_set"])


def load_graph(name: str) -> nx.MultiDiGraph:
    """Loads graph by name."""
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def save_graph(graph: nx.MultiDiGraph, path: str):
    nx.drawing.nx_pydot.write_dot(graph, path)


def get_graph_info_by_name(name: str) -> GraphInfo:
    return graph_info(load_graph(name=name))


def graph_info(graph: nx.MultiDiGraph) -> GraphInfo:
    """Returns summary about graph :class:`nx.MultiDiGraph`"""
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([d["label"] for _, _, d in graph.edges(data=True)]),
    )


def create_two_cycles_graph(
    n: int, m: int, labels: tuple = ("a", "b")
) -> nx.MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
