from typing import Tuple, Set, List

import cfpq_data
import networkx as nx

__all__ = [
    "Graph",
    "GraphDescription",
    "get_description",
    "get_two_cycles",
    "save_to_dot",
    "get_names",
]


class GraphDescription:
    """
    Encapsulates description of graph: name, number of nodes, number of edges, set of edge labels.

    Attributes
    ----------
    name: str
        Name of graph
    nodes: int
        Number of graph nodes
    edges: int
        Number of graph edges
    edge_labels: Set[str]
        Graph edge labels set
    """

    def __init__(self, name, nodes: int, edges: int, edge_labels: Set[str]):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.edge_labels = edge_labels

    def __str__(self):
        return (
            f"- number of nodes: {str(self.nodes)}\n"
            + f"\t- number of edges: {str(self.edges)}\n"
            + f"\t- edge labels: {str(self.edge_labels)}"
        )


class Graph:
    """
    Encapsulates graph: graph object and it's description.

    Attributes
    ----------
    graph: MultiDiGraph
        Graph object
    description: GraphDescription
        Description of graph object
    """

    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph
        self.description = GraphDescription(
            graph.name,
            graph.number_of_nodes(),
            graph.number_of_edges(),
            cfpq_data.get_labels(graph, verbose=False),
        )

    def __str__(self):
        return f"""
            Graph {self.description.name}:
            {str(self.description)}
            """

    def set_name(self, name):
        self.description.name = name


pool = list()


def get_description(name: str) -> GraphDescription:
    """
    Gets a description of real dataset graph encapsulated in GraphDescription.

    Parameters
    ----------
    name: str
        Name of the graph from https://jetbrains-research.github.io/CFPQ_Data/dataset/index.html

    Returns
    -------
    GraphDescription
        Description of graph

    Raises
    ------
    NameError
        If name not in https://jetbrains-research.github.io/CFPQ_Data/dataset/index.html
    """

    graph = cfpq_data.graph_from_dataset(name, verbose=False)

    if graph is None:
        raise NameError(
            f'Wrong dataset graph name "{name}", please specify it by real dataset name'
        )

    current = Graph(graph)
    current.set_name(name)

    global pool
    pool.append(current)

    return current.description


def get_two_cycles(
    first_cycle: int, second_cycle: int, edge_labels: Tuple[str, str]
) -> Graph:
    """
    Generates two cycles graph specified by parameters.

    Parameters
    ----------
    first_cycle: int
        Number of nodes in the first cycle
    second_cycle: int
        Number of nodes in the second cycle
    edge_labels: Tuple[str, str]
        Labels for edges on the first and second cycles

    Returns
    -------
    Graph
        Class encapsulates graph
    """

    graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle, second_cycle, edge_labels=edge_labels, verbose=False
    )

    current = Graph(graph)
    current.set_name("two_cycles")

    global pool
    pool.append(current)

    return current


def save_to_dot(
    path: str, name: str = None, graph: nx.MultiDiGraph = None
) -> GraphDescription:
    """
    Saves graph by name or passed graph to "*.dot" file specified by path.

    If all optional parameters specified, name has higher priority.

    If no optional parameters specified, the last used graph saves.
    But if list of graphs is empty, it raises an exception.

    Parameters
    ----------
    path: str
        Path to save the graph, extension ".dot" required
    name: str, default = None
        Name one of the used graphs
    graph: networkx.MultiDiGraph, default = None
        Graph to save

    Returns
    -------
    GraphDescription
        Description of graph

    Raises
    ------
    IndexError
        If it's no graphs in list to save
    NameError
        If name specified with wrong value
    """

    global pool
    current = None

    if name is None:
        if graph is None:
            if len(pool) > 0:
                current = pool[0]
                nx.drawing.nx_pydot.write_dot(current.graph, path)
            else:
                raise IndexError("No graphs in list to save: add something to it")
        else:
            current = Graph(graph)
            # graph_pool.append(current)
            nx.drawing.nx_pydot.write_dot(current.graph, path)
    else:
        for g in pool:
            if g.description.name == name:
                current = g

        if current is None:
            if graph is None:
                raise NameError(
                    f'Wrong graph name: make sure that "{name}" graph has been used'
                )
            else:
                current = Graph(graph)
                # graph_pool.append(current)
                nx.drawing.nx_pydot.write_dot(current.graph, path)

        nx.drawing.nx_pydot.write_dot(current.graph, path)

    return current.description


def get_names() -> List[str]:
    """
    Gets names list of ever used graphs

    Returns
    -------
    List[str]
        Names of ever used graphs
    """

    names = []
    for g in pool:
        names.append(g.description.name)

    return names
