import cfpq_data
import networkx as nx


def get_graph_info(name: str):
    """Load a graph by name. Passes through it and add unique labels to set.

    :return: 3-tuple (number of nodes, number of edges, all unique edge labels)
    or None if file with passed name is not found

    """

    try:
        graph_path = cfpq_data.download(name)
        graph = cfpq_data.graph_from_csv(graph_path)
    except FileNotFoundError:
        print("File {name} not found".format(name=name))
        return

    s = set()
    for i in dict(graph.edges).values():
        for j in i.values():
            s.add(j)

    return graph.number_of_nodes(), graph.number_of_edges(), s


def two_cycles_graph_to_file(n1: int, n2: int, labels: tuple, filename: str):
    """Generate two cycles graph and save it to dot file.

    :param n1: number of nodes in first cycle
    :param n2: number of nodes in second cycle
    :param labels: 2-tuple, where elements mark first and second cycles of graph according
    :param filename: name of file to save
    :return: None

    """
    g = cfpq_data.graphs.generators.labeled_two_cycles_graph(n1, n2, labels=labels)
    graph = nx.drawing.nx_pydot.to_pydot(g)
    graph.write(filename)
