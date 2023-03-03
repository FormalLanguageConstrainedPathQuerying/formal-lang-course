from pathlib import Path
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
        return cls.open_graph(cfpq_data.download(name))

    @classmethod
    def open_graph(cls, path: Path) -> MultiDiGraph:
        return cfpq_data.graph_from_csv(path)

    @classmethod
    def write_graph_to_dot_file(cls, graph: MultiDiGraph, file_path: str):
        nx_pydot.write_dot(graph, file_path)

    @classmethod
    def graph_info_by_name(cls, name: str) -> GraphInfo:
        # Returning number of nodes, number of edges, label of graph by graph name
        graph = cls.download_graph(name)
        return cls.GraphInfo(
            graph.number_of_nodes(),
            graph.number_of_edges(),
            cfpq_data.get_sorted_labels(graph),
        )

    @classmethod
    def create_two_cycle_labeled_graph(
        cls,
        number_of_nodes_in_cycle_a: int,
        number_of_nodes_in_cycle_b: int,
        labels: tuple[str, str],
    ) -> MultiDiGraph:
        # Builds two cycle graph with its labels
        return cfpq_data.labeled_two_cycles_graph(
            number_of_nodes_in_cycle_a, number_of_nodes_in_cycle_b, labels=labels
        )

    @classmethod
    def create_two_cycle_labeled_graph_and_save(
        cls,
        number_of_nodes_in_cycle_a: int,
        number_of_nodes_in_cycle_b: int,
        labels: tuple[str, str],
        file_path: str,
    ) -> None:
        # Builds two cycle graph with its labels, saves graph with dot file
        cls.write_graph_to_dot_file(
            cls.create_two_cycle_labeled_graph(
                number_of_nodes_in_cycle_a,
                number_of_nodes_in_cycle_b,
                labels,
            ),
            file_path,
        )
