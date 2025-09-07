# Task 1: Graph Processing
import cfpq_data
import networkx


class GraphReport:
    def __init__(self, edges_num, nodes_num, labels):
        self.edges_num = edges_num
        self.nodes_num = nodes_num
        self.labels = labels


def process_graph(name) -> GraphReport:
    graph_path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return GraphReport(edges_num=graph.number_of_nodes(), nodes_num=graph.number_of_edges(),
                       labels=cfpq_data.get_sorted_labels(graph), )


def save_graph(cycle_nodes_num, labels, path):
    networkx.nx_pydot.write_dot(
        cfpq_data.labeled_two_cycles_graph(cycle_nodes_num[0], cycle_nodes_num[1], labels=labels), path)
