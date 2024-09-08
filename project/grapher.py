import cfpq_data as cfpq
from typing import Tuple
import networkx as nx


class GraphData:
    # Function 1 from task 1
    def __init__(self, name: str):
        csv_path = cfpq.download(name)
        graph = cfpq.graph_from_csv(csv_path)

        self.__nodes_count = graph.number_of_nodes()
        self.__edges_count = graph.number_of_edges()
        self.__labels = cfpq.get_sorted_labels(graph)

    @property
    def nodes(self):
        return self.__nodes_count

    @property
    def edges(self):
        return self.__edges_count

    @property
    def edge_labels(self):
        return list(self.__labels)


# Graph saver
def save_graph_pydot(path: str, graph: nx.MultiDiGraph):
    pydot_graph = nx.nx_pydot.to_pydot(graph)
    pydot_graph.write_dot(path)


# Function 2 from task 1
def create_graph_with_cycles(path: str, n: int, m: int, labels: Tuple[str, str]):
    """
    @param path: Path where to save the graph
    @param n: The number of nodes in the first cycle without a common node
    @param m: The number of nodes in the second cycle without a common node
    @param labels: Labels that will be used to mark the edges of the graph
    """

    graph = cfpq.labeled_two_cycles_graph(n, m, labels=labels)
    save_graph_pydot(graph)
