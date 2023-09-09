import networkx as nx
import cfpq_data as cfpq

from project.cfpq.graph_info import GraphInfo


def get_graph_info(graph: nx.Graph) -> GraphInfo:
    number_of_nodes = graph.number_of_nodes()
    number_of_edges = graph.number_of_edges()
    unique_labels = set(map(lambda data: data[2], graph.edges.data(data="label")))

    return GraphInfo(number_of_nodes, number_of_edges, unique_labels)


def create_labeled_two_cycles_graph(
    first_cycle: (int, str),
    second_cycle: (int, str),
) -> nx.MultiDiGraph:
    return cfpq.labeled_two_cycles_graph(
        n=first_cycle[1],
        m=second_cycle[1],
        labels=(first_cycle[2], second_cycle[2]),
    )
