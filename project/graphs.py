from typing import Tuple

import cfpq_data
import networkx


class GraphInfo:
    def __init__(self, nodes_count, edges_count, labels):
        self.edges_count = edges_count
        self.nodes_count = nodes_count
        self.labels = labels


def get_graph_info(graph):
    return GraphInfo(
        graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_labels(graph)
    )


def generate_and_save_two_cycles(
    first_cycle_nodes_num, second_cycle_nodes_num, labels: Tuple[str, str], filename
):
    graph_generated = cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes_num, second_cycle_nodes_num, edge_labels=labels, verbose=False
    )
    graph = networkx.drawing.nx_pydot.to_pydot(graph_generated)
    graph.write_raw(filename)
