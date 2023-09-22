import cfpq_data
import pydot

__all__ = ["GraphInfo", "get_graph_stats", "generate_two_cycles_graph"]


class GraphInfo:

    """class for info about graphs: number of nodes and edges and list of possible edge labels"""

    def __init__(self):
        self.nodes = 0
        self.edges = 0
        self.labels = []

    def __init__(self, nodes, edges, labels):
        self.nodes = nodes
        self.edges = edges
        self.labels = labels


def get_graph_stats(graph_name):

    """gets info about a graph from its name"""

    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    labels = cfpq_data.get_sorted_labels(graph)
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()

    return GraphInfo(nodes, edges, labels)


def generate_two_cycles_graph(n1, n2, label1, label2, file_name, graph_name="G"):

    """generates a graph with two cycles of length n1 and n2, with labels label1 and label2 on edges of each cycle"""

    cfpq_graph = cfpq_data.labeled_two_cycles_graph(n1, n2, labels=(label1, label2))
    dot_graph = pydot.Dot(graph_name)
    edges = list(cfpq_graph.edges(data=True))
    for edge in edges:
        start, end, data = edge
        dot_graph.add_edge(pydot.Edge(start, end, label=data["label"]))

    dot_graph.write_raw(file_name)
