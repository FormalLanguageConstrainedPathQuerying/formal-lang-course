from typing import NamedTuple
import cfpq_data
from networkx import MultiDiGraph
from networkx.drawing import nx_pydot


class GraphUtils(object):
    class GraphInfo(NamedTuple):
        number_of_nodes: int
        number_of_edges: int
        sorted_labels: list[str]

    @classmethod
    def download_graph(cls, name: str) -> MultiDiGraph:
        return cfpq_data.graph_from_csv(cfpq_data.download(name))

    @classmethod
    def write_graph_to_dot_file(cls, graph: MultiDiGraph, file_path: str):
        nx_pydot.write_dot(graph, file_path)

    @classmethod
    def graph_info_by_name(cls, name: str) -> GraphInfo:
        # По имени графа возвращает количество вершин, рёбер и перечисление различные метки, встречающиеся на рёбрах.
        graph = cls.download_graph(name)
        return cls.GraphInfo(
            graph.number_of_nodes(),
            graph.number_of_edges(),
            cfpq_data.get_sorted_labels(graph),
        )

    @classmethod
    def create_two_cycle_labeled_graph_and_save(
        cls,
        number_of_nodes_in_cycle_a: int,
        number_of_nodes_in_cycle_b: int,
        labels: tuple[str, str],
        file_path: str,
    ) -> None:
        # По количеству вершин в циклах и именам меток строит граф из двух циклов и сохраняет его в указанный файл в формате DOT.
        graph = cfpq_data.labeled_two_cycles_graph(
            number_of_nodes_in_cycle_a, number_of_nodes_in_cycle_b, labels=labels
        )
        cls.write_graph_to_dot_file(graph, file_path)
