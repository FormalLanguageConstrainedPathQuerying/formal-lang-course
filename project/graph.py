import cfpq_data
import pathlib

import networkx as nx
from typing import Set, Tuple


def get_graph_label(graph: nx.MultiDiGraph) -> Set[str]:
    return set(edge_data[2] for edge_data in graph.edges.data("label"))


def get_graph_info_by_name(name: str) -> Tuple[int, int, Set[str]]:
    graph_path: pathlib.Path = cfpq_data.download(name)
    graph: nx.MultiDiGraph = cfpq_data.graph_from_csv(graph_path)

    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        get_graph_label(graph=graph),
    )


def create_labeled_two_cycles_graph(
    n: int, m: int, labels: Tuple[str, str], path: str, **kwargs
) -> None:
    graph: nx.MultiDiGraph = cfpq_data.labeled_two_cycles_graph(
        n=n, m=m, labels=labels, **kwargs
    )
    nx.drawing.nx_pydot.write_dot(G=graph, path=path)
