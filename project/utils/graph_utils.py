import cfpq_data
from networkx import MultiDiGraph
from collections import namedtuple

GraphInfo = namedtuple('GraphInfo', 'nodes_num edges_num labels')
"""
Namedtuple of number of nodes, number of edges, set of edges' labels
"""


def get_graph(name: str) -> MultiDiGraph:
    """
    Finds graph with a given name.

    :param name: Name of graph to find.
    :return: Existing graph with a given name from CFPQ_Data Dataset.
    :raises FileNotFoundError: if no graph with given name found.
    """
    graph_path = cfpq_data.dataset.download(name)
    graph = cfpq_data.graph_from_csv(graph_path)

    return graph


def get_graph_info(name: str) -> GraphInfo:
    """
    Show basic info of a graph with a given name from CFPQ_Data Dataset.

    :param name: Name of graph to find.
    :return: Namedtuple of number of nodes, number of edges, set of edges' labels
    :raises FileNotFoundError: if no graph with given name found.
    """
    graph = get_graph(name)
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([i[2]['label'] for i in graph.edges.data(default=True)])
    )
