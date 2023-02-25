from ast import Tuple
import cfpq_data as cd
import networkx as nx


def load_graph_by_name(name: str) -> nx.MultiDiGraph:
    path_to_graph = cd.download(name)
    graph = cd.graph_from_csv(path_to_graph)
    return graph


def number_of_nodes(graph: nx.MultiDiGraph) -> int:
    return graph.number_of_nodes()


def number_of_edges(graph: nx.MultiDiGraph) -> int:
    return graph.number_of_edges()


def unique_labels(graph: nx.MultiDiGraph):
    labels = set()
    for edge_info in graph.edges(data="label"):
        if edge_info:
            labels.add(edge_info[2])
    return labels


def generate_two_cycles_graph(
    edges_number_1: int, edges_number_2: int, labels, path_to_save: str = None
) -> nx.MultiDiGraph:
    graph = cd.labeled_two_cycles_graph(edges_number_1, edges_number_2, labels=labels)
    if path_to_save:
        nx.nx_pydot.write_dot(graph, path_to_save)
    return graph
