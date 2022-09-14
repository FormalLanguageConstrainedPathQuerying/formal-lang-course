import cfpq_data
import networkx


def load_graph(name: str):
    """
    Load graph by its name and returns it

    Parameters
    ----------
    name : str
        The name of graph

    Returns
    -------
    networkx.MultiDiGraph
        Loaded graph

    Raises
    ----------
    FileNotFoundError
        If failed to found graph with such name
    """
    try:
        graph_path = cfpq_data.download(name)
        return cfpq_data.graph_from_csv(graph_path)
    except FileNotFoundError as e:
        raise e


def get_graph_info(name: str):
    """
    Returns as tuple number of nodes, number of edges and list of all labels for graph with specified name

    Parameters
    ----------
    name : str
        The name of graph

    Returns
    -------

    tuple
        [num_of_nodes, num_of_edges, list_of_labels]
    """

    g = load_graph(name)

    labels = []

    for _, _, lbl in g.edges(data=True):
        labels.append(lbl["label"])

    return g.number_of_nodes(), g.number_of_edges(), labels


def create_and_save_two_cycles_graph(n, m, labels, path):
    """
    Creates two cycles graph and saves it to the specified .dot file

    :param n: Number of vertices in the first cycle
    :param m: Number of vertices in the second cycle
    :param labels: Names of labels
    :param path: Path to file
    :returns: None
    """
    g = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(g, path)
