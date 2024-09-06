from typing import Tuple

import cfpq_data
from networkx.drawing import nx_pydot
import networkx as nx


class Graph:
    @staticmethod
    def load_graph(name: str) -> nx.MultiDiGraph:
        try:
            graph_path = cfpq_data.download(name)
            return cfpq_data.graph_from_csv(graph_path)
        except FileNotFoundError:
            raise FileNotFoundError

    @staticmethod
    def graph_info(name: str):
        graph = Graph.load_graph(name)
        return graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_sorted_labels(graph)

    @staticmethod
    def create_labeled_graph(count_of_nodes: int,
                             count_of_edges: int,
                             label: Tuple[str, str],
                             path: str) -> None:
        graph = cfpq_data.labeled_two_cycles_graph(n=count_of_nodes, m=count_of_edges, labels=label)
        Graph.save_graph_dot(graph, path)

    @staticmethod
    def save_graph_dot(graph: nx.MultiDiGraph, path: str) -> None:
        grph = nx_pydot.to_pydot(graph)
        grph.write(path)
