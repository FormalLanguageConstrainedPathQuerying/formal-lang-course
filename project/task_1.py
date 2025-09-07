from pathlib import Path

import cfpq_data as cfpq
from networkx import MultiDiGraph as graph
from networkx.drawing.nx_pydot import to_pydot


class GraphParams:
    node_count: int
    edge_count: int
    labels: set

    def __init__(self, node_count: int, edge_count: int, labels: set):
        self.node_count = node_count
        self.edge_count = edge_count
        self.labels = labels

def load_graph(name: str) -> graph:
    path = cfpq.download(name)
    g = cfpq.graph_from_csv(path)

    return g

def get_graph_params(name: str) -> GraphParams:
    g = load_graph(name)

    return GraphParams(
        g.number_of_nodes(),
        g.number_of_edges(),
        set(cfpq.get_sorted_labels(g))
    )

def save_to_dot(g: graph, filename: Path | str):
    dot_graph = to_pydot(g)
    dot_graph.write_raw(filename)


def create_labeled_two_cycles_graph(
    cycles: tuple[int, int],
    labels: tuple[str, str],
    ):
    g = cfpq.labeled_two_cycles_graph(
        cycles[0],
        cycles[1],
        labels=labels
    )

    return g
