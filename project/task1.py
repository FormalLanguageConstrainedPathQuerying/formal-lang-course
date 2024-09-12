from dataclasses import dataclass
from typing import Any, Iterable, Tuple
import cfpq_data
from cfpq_data.graphs.generators import labeled_two_cycles_graph
import networkx as nx


@dataclass
class GraphInfo:
    node_count: int
    edge_count: int
    edge_labels: list[Any]


def get_graph_info_via_name(name: str) -> GraphInfo:
    graph_path = cfpq_data.download(name)
    G = cfpq_data.graph_from_csv(graph_path)

    node_count = len(G)
    edge_count = G.number_of_edges()
    edges_labels = cfpq_data.get_sorted_labels(G)

    return GraphInfo(
        node_count=node_count, edge_count=edge_count, edge_labels=edges_labels
    )


def save_labeled_two_cycles_graph(
    n: int | Iterable[Any],
    m: int | Iterable[Any],
    labels: Tuple[str, str],
    path_to_save: str,
):
    LTCG = labeled_two_cycles_graph(n=n, m=m, labels=labels)
    nx.drawing.nx_pydot.write_dot(LTCG, path_to_save)
