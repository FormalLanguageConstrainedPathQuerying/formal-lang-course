import cfpq_data
import networkx
import pydot


def get_graph(name):
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def save_labeled_two_cycle_graph(path, n, m, labels=("a", "b")):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(graph, path)
    return graph
