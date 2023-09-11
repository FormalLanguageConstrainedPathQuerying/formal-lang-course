from typing import Tuple
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot
import cfpq_data

from project.graph_data import GraphData


def download_graph(name: str) -> MultiDiGraph:
    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return graph


def save_graph(G: MultiDiGraph, path: str) -> None:
    write_dot(G, path)


def get_graph_data(G: MultiDiGraph) -> GraphData:
    def get_label(edge):
        return edge[2]

    labels = set(map(get_label, G.edges(data="label")))
    return GraphData(G.number_of_nodes(), G.number_of_edges(), labels)


def get_graph_data_by_name(name: str) -> GraphData:
    return get_graph_data(download_graph(name))


def create_labeled_two_cycle_graph(
    n: int, m: int, labels: Tuple[str, str]
) -> MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(n, m, 0, labels)


def create_labeled_two_cycle_graph_and_save(
    n: int, m: int, labels: Tuple[str, str], path: str
) -> None:
    G = create_labeled_two_cycle_graph(n, m, labels)
    save_graph(G, path)
