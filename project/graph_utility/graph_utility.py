from os import path
from pathlib import Path

import cfpq_data
import networkx


def load_graph(graph_name: str) -> networkx.MultiDiGraph:
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return graph


def get_graph_info(graph_name: str) -> tuple[int, int, set[str]]:
    graph = load_graph(graph_name)
    graph_labels = set(label for _, _, label in graph.edges.data(data="label"))
    graph_edges = graph.number_of_edges()
    graph_nodes = graph.number_of_nodes()
    return graph_edges, graph_nodes, graph_labels


def create_graph_of_two_cycles(
    first_cycle_nodes: int, second_cycle_nodes: int, labels: (str, str)
) -> networkx.MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(
        n=first_cycle_nodes, m=second_cycle_nodes, labels=labels
    )


def save_graph_as_dot(graph: networkx.Graph, output_name: str, output_path: str):
    networkx.drawing.nx_pydot.to_pydot(graph).write_raw(
        Path(path.join(output_path, output_name + ".dot"))
    )
