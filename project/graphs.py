from typing import Tuple

import cfpq_data
import networkx as nx


class GraphInfo:
    def __init__(self, nodes_count, edges_count, labels):
        self.edges_count = edges_count
        self.nodes_count = nodes_count
        self.labels = labels

    def __str__(self):
        return f"""
        Edges count: {str(self.edges_count)}
        Nodes count: {str(self.nodes_count)}
        Labels: {str(self.labels)}
    """


def get_graph_info(graph: nx.MultiDiGraph):
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_and_save_two_cycles(
    first_cycle_nodes_num: int,
    second_cycle_nodes_num: int,
    labels: Tuple[str, str],
    filename: str,
):
    graph_generated = cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes_num, second_cycle_nodes_num, edge_labels=labels, verbose=False
    )
    graph = nx.drawing.nx_pydot.to_pydot(graph_generated)
    graph.write_raw(filename)
