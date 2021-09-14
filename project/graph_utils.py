import cfpq_data
import networkx


def get_graph_description(graph: networkx.MultiDiGraph) -> (int, int, set):
    """Returns number of nodes, number of edges, set of labels

    :param graph: A directed graph class that can store multiedges
    :type graph: networkx.MultiDiGraph
    """

    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def write_two_cycles_graph(
    first_cycle_vertices: int, second_cycle_vertices, edge_labels: (str, str), path: str
) -> None:
    """Creates and writes a graph of two loops along a given path

    :param first_cycle_vertices: The number of nodes in the first cycle without a common node
    :type first_cycle_vertices: int
    :param second_cycle_vertices: The number of nodes in the second cycle without a common node
    :type second_cycle_vertices: int
    :param edge_labels: Labels that will be used to mark the edges of the graph
    :type edge_labels: (str, str)
    :param path: File path
    :type path: str
    """

    two_cycles_graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_vertices,
        second_cycle_vertices,
        edge_labels=edge_labels,
        verbose=False,
    )
    networkx.drawing.nx_pydot.write_dot(two_cycles_graph, path)
