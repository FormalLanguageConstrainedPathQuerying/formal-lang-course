from dataclasses import dataclass
from typing import Any
import cfpq_data
from cfpq_data.graphs.generators import labeled_two_cycles_graph
from networkx import MultiDiGraph
import networkx as nx


@dataclass
class GraphInfo:
    node_count: int
    edge_count: int
    edge_labels: list[Any]

    def create_labeled_two_cycles_graph(self) -> MultiDiGraph:
        G = labeled_two_cycles_graph(
            self.node_count, self.edge_count, labels=self.edge_labels
        )
        return G


def get_graph_info_via_name(name: str) -> GraphInfo:
    graph_path = cfpq_data.download(name)
    G = cfpq_data.graph_from_csv(graph_path)

    node_count = len(G)
    edge_count = G.number_of_edges()
    edges_labels = cfpq_data.get_sorted_labels(G)

    return GraphInfo(
        node_count=node_count, edge_count=edge_count, edge_labels=edges_labels
    )


def download_and_save_labeled_two_cycles_graph(name: str, path_to_save: str):
    graph_info = get_graph_info_via_name(name)
    LTCG = graph_info.create_labeled_two_cycles_graph()
    nx.drawing.nx_pydot.write_dot(LTCG, path_to_save)
