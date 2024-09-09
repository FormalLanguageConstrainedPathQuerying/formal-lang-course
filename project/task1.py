from dataclasses import dataclass
import cfpq_data
import networkx
from pathlib import Path
from typing import List, Any, Tuple


@dataclass
class GraphInfo:
    num_of_nodes: int
    num_of_edges: int
    labels: List[Any]


def load_graph_info(path: str) -> GraphInfo:
    graph_path = cfpq_data.download(path)
    graph = cfpq_data.graph_from_csv(graph_path)
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_sorted_labels(graph),
    )


def create_and_save_labeled_two_cycled_graph(
    n: int, m: int, labels: Tuple[str, str], output_path: Path
) -> None:
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.to_pydot(graph).write_raw(output_path)
