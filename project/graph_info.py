import cfpq_data, networkx
from typing import Tuple
from dataclasses import dataclass

@dataclass
class GraphInfo:
    node_num: int
    edge_num: int
    labels: list[str]

def get_graph_info(name: str) -> GraphInfo:
    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)

    node_n = graph.number_of_nodes()
    edges_n = graph.number_of_edges()

    labels = cfpq_data.get_sorted_labels(graph)

    return GraphInfo(node_n, edges_n, labels)

def save_two_cycle_graph(n: int, m: int, labels: Tuple[str, str], filepath: str) -> bool:
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    dotgraph = networkx.drawing.nx_pydot.to_pydot(graph)
    dotgraph.write_raw(filepath)
    return True
