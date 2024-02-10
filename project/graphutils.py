from cfpq_data import *
import networkx


def graph_signature(graph_name):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return (graph.number_of_nodes(), graph.number_of_edges(), get_sorted_labels(graph))


def save_twocycled_graph(vertices1, vertices2, labels):
    graph = labeled_two_cycles_graph(vertices1, vertices2, labels=labels)
    networkx.drawing.nx_pydot.write_dot(
        graph, "twocycled_" + str(vertices1) + "_" + str(vertices2) + ".dot"
    )
