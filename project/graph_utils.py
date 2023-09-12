from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Tuple, Any
from collections.abc import Iterable
from networkx.drawing.nx_pydot import to_pydot
import cfpq_data


@dataclass
class GraphInfo:
    number_of_nodes: int
    number_of_edges: int
    labels_set: set


class GraphUtils(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_graph_info(graph_name: str) -> GraphInfo:
        graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
        return GraphInfo(
            graph.number_of_nodes(),
            graph.number_of_edges(),
            set(cfpq_data.get_sorted_labels(graph)),
        )

    @staticmethod
    def save_labeled_two_cycles_graph(
        n: Union[int, Iterable[Any]],
        m: Union[int, Iterable[Any]],
        common_node: Union[int, Any],
        path: str,
        labels: Tuple[str, str] = ("a", "b"),
    ) -> None:
        # pylint: disable=E1101
        graph = cfpq_data.labeled_two_cycles_graph(
            n, m, common_node=common_node, labels=labels
        )
        to_pydot(graph).write_raw(path)
