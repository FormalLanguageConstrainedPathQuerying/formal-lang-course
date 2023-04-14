import cfpq_data as cfpq
import networkx as nx
from collections import namedtuple
from pyformlang.cfg import CFG

# graph info
GI = namedtuple("GI", ["n_c", "e_c", "ls"])


def info(g: nx.Graph) -> GI:
    """
    Returns an info about graph
    :param g: nx.Graph graph
    :return: GI
    """
    ls_s = set(ats["label"] for (a, b, ats) in g.edges.data())
    return GI(len(g.nodes), len(g.edges), list(ls_s))


def from_dataset(path: str) -> GI:
    """
    Returns graph info from csv on path
    :param path: path to csv file
    :return: GI
    """
    return info(cfpq.graph_from_csv(cfpq.download(path)))


def save(g: nx.Graph, path: str):
    """
    Saves graph to path
    :param g: nx.Graph graph
    :param path: path to save
    :return: void
    """
    nx.drawing.nx_pydot.to_pydot(g).write_raw(path)


def two_cycled_graph_again_and_again(fp: str, fl: str, fn: int, sn: int, sl: str):
    """
    Creates two cycled graph with provided parameters and writes it to path
    :param fp: file path
    :param fl: label of edges in first cycle
    :param fn: number of nodes in first cycle
    :param sn: number of nodes in second cycle
    :param sl: label of edges in second cycle
    :return: void
    """
    save(cfpq.labeled_two_cycles_graph(fn, sn, labels=(fl, sl)), fp)


def parse(p: str) -> CFG:
    """
    Parses CFG
    :param p: file path
    :return: CFG
    """
    with open(p, "r") as f:
        ct = f.read()
        return CFG.from_text(ct)


def to_weak_homsky_form(cfg: CFG) -> CFG:
    """
    Converts CFG to weak Homsky form
    :param cfg: CFG
    :return: CFG
    """
    nf = cfg.remove_useless_symbols().eliminate_unit_productions().remove_useless_symbols()
    w = set(nf._decompose_productions(nf._get_productions_with_only_single_terminals()))
    return CFG(start_symbol=nf.start_symbol, productions=w)
