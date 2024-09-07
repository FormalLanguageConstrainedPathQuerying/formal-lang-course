from typing import Tuple
import cfpq_data
import networkx as nx
from networkx.drawing import nx_pydot
from dataclasses import dataclass

@dataclass
class GraphInfo:
    nodes_count: int
    edges_count: int
    edge_labels: list

def get_graph_info(name: str) -> GraphInfo:
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    edge_labels = list(map(lambda edge: list(edge[2].values()), graph.edges(data=True)))
    unique_labels = set()
    for labels in edge_labels:
        for label in labels:
            unique_labels.add(label)
    result_labels = list(unique_labels)
    result_labels.sort()

    return GraphInfo(graph.number_of_nodes(), graph.number_of_edges(), result_labels)

def save_two_cycles_graph(n: int, m: int, path: str, labels: Tuple[str, str] = ("A", "B")) -> None:
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    pydot_graph = nx_pydot.to_pydot(graph)
    pydot_graph.write(path)