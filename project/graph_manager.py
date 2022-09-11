from cfpq_data import *
from networkx import MultiDiGraph, nx_pydot


class GraphManager:
    @staticmethod
    def get_info(name: str) -> tuple[int, int, list[str]]:
        graph = GraphManager.__get_graph(name)
        labels = GraphManager.__get_labels(graph)
        return graph.number_of_nodes(), graph.number_of_edges(), labels

    @staticmethod
    def create_two_cycle_labeled_graph(
        sizes: tuple[int, int], labels: tuple[str, str], path: str
    ) -> None:
        graph = GraphManager.__create_two_cycle_labeled_graph(sizes, labels)
        nx_pydot.write_dot(graph, path)

    @staticmethod
    def __get_graph(name: str) -> MultiDiGraph:
        path = cfpq_data.download(name)
        return cfpq_data.graph_from_csv(path)

    @staticmethod
    def __get_labels(graph: MultiDiGraph) -> list[str]:
        labels = []
        [
            labels.append(edge[2]["label"])
            for edge in graph.edges(data=True)
            if (edge[2]["label"]) not in labels
        ]
        return labels

    @staticmethod
    def __create_two_cycle_labeled_graph(
        dimensions: tuple[int, int], labels: tuple[str, str]
    ) -> MultiDiGraph:
        return cfpq_data.labeled_two_cycles_graph(
            n=dimensions[0], m=dimensions[1], labels=labels
        )
