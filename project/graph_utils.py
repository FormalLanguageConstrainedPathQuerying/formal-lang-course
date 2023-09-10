from typing import Any, Tuple, List
from pathlib import Path
import cfpq_data
import networkx as nx


def get_graph_info(name: str) -> Tuple[int, int, List[Any]]:
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        list(set(cfpq_data.get_sorted_labels(graph))),
    )


def generate_two_cycles_graph(
    first_cycle_nodes: int, second_cycle_nodes: int, labels: Tuple[str, str]
) -> nx.MultiDiGraph:
    return cfpq_data.graphs.labeled_two_cycles_graph(
        first_cycle_nodes, second_cycle_nodes, labels=labels
    )


def save_graph_in_dot(graph: nx.MultiDiGraph, path: Path | str) -> None:
    dot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    dot_graph.write(path)
