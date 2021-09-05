"""
A set of methods for working with a graph.
"""

import cfpq_data
import networkx

__all__ = ["get_graph_info", "generate_and_export_two_cycle"]


def get_graph_info(graph: networkx.MultiDiGraph) -> (int, int, set):
    """
    Return inforamtion about passed graph.
    :param graph:
    :return:
    """
    return graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_labels(graph)


def create_two_cycle_graph(
    first_vertices: int, second_vertices: int, edge_labels: (str, str)
):
    """
    Create two cycle graphs by amount of vertices in first cycle and second and labels for each cycles.
    :param first_vertices:
    :param second_vertices:
    :param edge_labels:
    :return:
    """
    return cfpq_data.labeled_two_cycles_graph(
        first_vertices, second_vertices, edge_labels=edge_labels, verbose=False
    )


def get_pydot(graph):
    """
    Translate graph to DOT script.
    :param graph:
    :return:
    """
    return networkx.drawing.nx_pydot.to_pydot(graph)


def generate_and_export_two_cycle(
    first_vertices: int, second_vertices: int, edge_labels: (str, str), filename: str
):
    """
    Generate two cycle graph by amount of vertices in first cycle and second and labels for each cycles.
    And then export this graph as DOT script to file.
    :param first_vertices:
    :param second_vertices:
    :param edge_labels:
    :param filename:
    :return:
    """
    graph = create_two_cycle_graph(first_vertices, second_vertices, edge_labels)
    dot_script = networkx.drawing.nx_pydot.to_pydot(graph)
    dot_script.write(filename)
