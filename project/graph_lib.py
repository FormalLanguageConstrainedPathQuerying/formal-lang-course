from dataclasses import dataclass
from typing import Iterable, Any
import cfpq_data
import networkx as nx


@dataclass
class GraphInfo:
    nodes_count: int
    edges_count: int
    edge_labels: set


def get_graph_info_by_name(graph_name: str) -> GraphInfo:
    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    return GraphInfo(
        nodes_count=graph.number_of_nodes(),
        edges_count=graph.number_of_edges(),
        edge_labels={label for _, _, label in graph.edges(data="label")},
    )


def create_labeled_two_cycles_graph(
    fst_cycle_nodes: int | Iterable[Any],
    snd_cycle_nodes: int | Iterable[Any],
    common_node: int | Any,
    lebels_names: tuple[str, str],
    path: str,
) -> None:
    graph = cfpq_data.labeled_two_cycles_graph(
        fst_cycle_nodes, snd_cycle_nodes, common_node=common_node, labels=lebels_names
    )
    nx.drawing.nx_pydot.to_pydot(graph).write(path)
    return None
