from networkx import Graph, MultiDiGraph, drawing
import cfpq_data

class GraphInfo:
    """Graph info.

    Attributes
    ----------
    number_of_nodes : int
        The number of nodes in the graph.
    number_of_edges : int
        The number of edges in the graph.
    unique_labels : set[str]
        The set of labels in the graph.
    """

    number_of_nodes: int = 0
    number_of_edges: int = 0
    labels: set[str] = set()
    
def get_graph_info(graph: Graph) -> GraphInfo:
    """Get graph info.

    Parameters
    ----------
    graph : Graph
        The graph from which to get the info.

    Returns
    -------
    graph_info : GraphInfo
        The graph info.
    """
    number_of_nodes = graph.number_of_nodes()
    number_of_edges = graph.number_of_edges()
    
    labels = {label for _, _, label in graph.edges.data(data="label")}

    return GraphInfo(number_of_nodes, number_of_edges, labels)


def load_graph(graph_name : str) -> MultiDiGraph:
    """Load graph from dataset csv
    
    Parameters:
    ----------
    graph_name (str): 
        The name of the graph dataset to load.
        
    Examples
    --------
    >>> import
    >>> graph = load_graph('example')
    
    Returns:
    ----------
    nx.MultiDiGraph
    """
    
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    
    return graph

def create_and_save_dot(
    len1: int, len2: int, path: str, labels: tuple[str, str]) -> None:
    """
    Create a graph with cycles in DOT format and save it to a file.

    Parameters:
    ----------
    num_vertices of first cecles (int): The number of vertices in the graph.
    num_vertices of second cecles (int): The number of vertices in the graph.
    labels (tuple[str, str])): A tuple of edge labels to be used in the graph.
    save_path (str): The name of the output file where the DOT representation of the graph will be saved.

    Returns:
    ----------
    None
    """
    
    graph = cfpq_data.labeled_two_cycles_graph(len1, len2, labels=labels)
    data = drawing.nx_pydot.to_pydot(graph)
    data.write_raw(path)