from cfpq_data import *
import networkx.drawing.nx_pydot
from networkx import MultiDiGraph


def load_graph(name: str) -> MultiDiGraph:
    path = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path)


def graph_info(name: str):
    graph = load_graph(name)
    V = graph.number_of_nodes()  # count of node
    E = graph.number_of_edges()  # count of edges
    L = cfpq_data.get_sorted_labels(graph)  # label
    return V, E, L


def create_graph(
    first_circle_vertex_count, second_circle_vertex_count, labels, filename: str
):
    graph = cfpq_data.labeled_two_cycles_graph(
        first_circle_vertex_count, second_circle_vertex_count, labels=labels
    )
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    if not filename.endswith(".dot"):
        filename = filename + ".dot"
    with open(filename, "w"):
        pydot_graph.write(filename)
