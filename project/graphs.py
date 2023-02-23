import cfpq_data as cfpq
import networkx as nx
from collections import namedtuple

GraphInfo = namedtuple("GraphInfo", ["number_of_nodes", "number_of_edges", "edges"])


def get_graph_info(name: str) -> GraphInfo:
    path = cfpq.download(name)
    g = cfpq.graph_from_csv(path)
    return GraphInfo(g.number_of_nodes(), g.number_of_edges(), g.edges(data=True))


def save_two_cycles(path: str, n: int, m: int, labels=("a", "b")):
    g = cfpq.labeled_two_cycles_graph(n=n, m=m, labels=labels)
    dot = nx.drawing.nx_pydot.to_pydot(g)
    dot.write_raw(path)
