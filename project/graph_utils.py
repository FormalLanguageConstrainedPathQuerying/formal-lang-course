from dataclasses import dataclass
from pathlib import Path
import cfpq_data
import networkx as nx


@dataclass
class GraphProperties:
    """
    A class representing the properties of a graph.

    Attributes:
        node_count (int): The number of nodes in the graph.
        edge_count (int): The number of edges in the graph.
        labels (set[str]): A set of labels used on the graph's edges.
    """

    node_count: int
    edge_count: int
    labels: set[str]


def load_graph_properties_by_name(name: str) -> GraphProperties:
    """
    Loads a graph by its name and returns its key properties.

    Args:
        name (str): The name of the graph to load.

    Returns:
        GraphProperties: An object containing the number of nodes,
        edges, and labels present in the graph.

    Example:
        properties = load_graph_properties_by_name("example_graph")
        print(properties.node_count, properties.edge_count, properties.labels)
    """
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    node_count = graph.number_of_nodes()
    edge_count = graph.number_of_edges()
    labels = set(cfpq_data.get_sorted_labels(graph))

    return GraphProperties(node_count=node_count, edge_count=edge_count, labels=labels)
