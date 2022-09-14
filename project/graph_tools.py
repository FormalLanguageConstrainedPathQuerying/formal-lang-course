import cfpq_data


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
    # g = cfpq_data.labeled_cycle_graph(5, label="a")
    labels = []

    for _, _, lbl in g.edges(data=True):
        labels.append(lbl["label"])

    return g.number_of_nodes(), g.number_of_edges(), labels


print(get_graph_info("1"))
