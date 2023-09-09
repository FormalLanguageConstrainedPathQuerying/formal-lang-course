import cfpq_data as cfpq
import networkx as nx


def load_graph_by_name(name: str) -> nx.MultiDiGraph:
    """Load a graph by its name from the dataset.

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Returns
    -------
    graph : MultiDiGraph
        The graph data.
    """
    return cfpq.graph_from_csv(path=(cfpq.download(name)))


def save_graph_as_dot_file(graph: nx.Graph, path: str) -> bool:
    from networkx.drawing.nx_pydot import to_pydot as graph_to_dot

    return graph_to_dot(graph).write(path)
