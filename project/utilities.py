import cfpq_data
import networkx

from project.graph_info import GraphInfo


def get_graph_info(name):
    graph = cfpq_data.graph_from_csv(cfpq_data.download(name))
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([edge[2]["label"] for edge in graph.edges(data=True)]),
    )


def generate_two_cycles_graph(n, m, labels, path):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(graph, path)
