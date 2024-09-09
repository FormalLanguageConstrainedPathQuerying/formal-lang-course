import cfpq_data
import networkx

from typing import Tuple
from dataclasses import dataclass


@dataclass
class Graph:
    edges_cnt: int
    nodes_cnt: int
    labels: list


def load_graph(graph_name: str):
    path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path)
    edges_cnt = graph.number_of_edges()
    nodes_cnt = graph.number_of_nodes()
    labels = cfpq_data.get_sorted_labels(graph)
    return Graph(edges_cnt, nodes_cnt, labels)


def build_two_cycle_graph(n: int, m: int, labels: Tuple[str, str], path="./test2.dot"):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write_raw(path)
