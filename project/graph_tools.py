from pathlib import Path
from typing import *
from dataclasses import dataclass
import cfpq_data
import networkx as nx


@dataclass
class GraphData:
    nodes_count: int
    edges_count: int
    labels: set

    @staticmethod
    def get_graph_data_by_name(name: str) -> "GraphData":
        graph_path = cfpq_data.download(name)
        graph = cfpq_data.graph_from_csv(graph_path)
        return GraphData(
            nodes_count=graph.number_of_nodes(),
            edges_count=graph.number_of_edges(),
            labels=set(cfpq_data.get_sorted_labels(graph)),
        )


def save_graph_to_dot(graph: nx.MultiGraph, path: Path):
    nx.nx_pydot.to_pydot(graph).write_raw(path)


def create_and_save_two_cycle_graph(
    nodes_first_cycle_count: int,
    nodes_second_cycle_count: int,
    labels: tuple[str, str],
    path: Path,
):
    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_first_cycle_count, nodes_second_cycle_count, labels=labels
    )
    save_graph_to_dot(graph, path)
