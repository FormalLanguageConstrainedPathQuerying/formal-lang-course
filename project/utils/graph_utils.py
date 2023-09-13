import cfpq_data
import networkx

from cfpq_data import *
from networkx import MultiDiGraph


class GraphData:
    num_of_nodes: int
    num_of_edges: int
    set_of_labels: set

    def __init__(self, nodes: int, edges: int, labels: set):
        self.num_of_nodes = nodes
        self.num_of_edges = edges
        self.set_of_labels = labels


def load_graph(name: str) -> MultiDiGraph:
    bzip_graph = cfpq_data.graph_from_csv(path=(cfpq_data.download(name)))
    return bzip_graph


def get_graph_data(graph: MultiDiGraph) -> GraphData:
    return GraphData(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set(i for _, _, i in graph.edges.data("label")),
    )


def build_two_cycles_graph(
    n: int, m: int, label_names: tuple[str, str]
) -> MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(n, m, labels=label_names)


def draw_graph(graph: MultiDiGraph, path: str):
    networkx.drawing.nx_pydot.to_pydot(graph).write(path)
