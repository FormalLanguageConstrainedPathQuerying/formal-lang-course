import cfpq_data
from dataclasses import dataclass
from typing import List, Any
from pathlib import Path
import networkx as nx


@dataclass
class GraphData:
    node_count: int
    edge_count: int
    labels: List[Any]


def get_graph_data(name: str) -> GraphData:
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    return GraphData(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_sorted_labels(graph),
    )


def save_graph(graph: nx.MultiDiGraph, path: Path):
    pydot_graph = nx.nx_pydot.to_pydot(graph)
    pydot_graph.write_raw(path)


def save_labeled_two_cycles_graph(n: int, m: int, labels: List[Any], path: Path):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    save_graph(graph, path)
