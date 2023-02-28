import cfpq_data as cfpq
import networkx as nx
from collections import namedtuple

GraphInfo = namedtuple("GraphInfo", ["number_of_nodes", "number_of_edges", "edges"])


def get_graph_by_name(name: str) -> nx.MultiDiGraph:
    path = cfpq.download(name)
    g = cfpq.graph_from_csv(path)
    return g


def make_two_cycles(n: int, m: int, labels=("a", "b")):
    return cfpq.labeled_two_cycles_graph(n=n, m=m, labels=labels)


def get_graph_info(name: str) -> GraphInfo:
    g = get_graph_by_name(name)
    gi = GraphInfo(g.number_of_nodes(), g.number_of_edges(), g.edges(data=True))
    return gi


def save_graph(path: str, g: nx.MultiDiGraph):
    dot = nx.drawing.nx_pydot.to_pydot(g)
    dot.write_raw(path)


def save_two_cycles(path: str, n: int, m: int, labels=("a", "b")):
    g = make_two_cycles(n=n, m=m, labels=labels)
    save_graph(path, g)
