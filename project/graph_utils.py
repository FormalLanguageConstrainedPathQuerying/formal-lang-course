from dataclasses import dataclass

from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot

import cfpq_data

__all__ = ["GraphData", "from_named_graph", "write_labeled_two_cycles_graph"]


@dataclass
class GraphData:
    number_of_nodes: int
    number_of_edges: int
    labels: set[str]


def from_graph(graph: MultiDiGraph) -> GraphData:
    return GraphData(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([edge[2]["label"] for edge in graph.edges(data=True)]),
    )


def from_named_graph(name: str) -> GraphData:
    """
    Extracts graph data from named graph inside CFPQ Data Dataset

    :param name: name of graph to find in CFPQ Data Dataset
    :return: GraphData object filled with named graph data
    :raises FileNotFoundError: if graph with given name not found inside CFPQ Data Dataset
    """
    path = cfpq_data.dataset.download(name)
    return from_graph(cfpq_data.graph_from_csv(path))


def write_labeled_two_cycles_graph(
    sizes: tuple[int, int], labels: tuple[str, str], path: str
):
    """
    Generates cfpq_data.labeled_two_cycles_graph in file with given sizes of cycles and given labels on edges

    :param sizes: sizes for each cycle
    :param labels: labels for edges in each cycle
    :param path: output path where graph will be written in DOT format
    """
    n, m = sizes
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    write_dot(graph, path)
