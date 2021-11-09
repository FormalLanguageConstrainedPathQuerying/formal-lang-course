from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.grammars.hellings import hellings
from project.utils.CFG_utils import transform_cfg_to_wcnf

__all__ = ["cfpq"]


def cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_var: Variable = Variable("S"),
) -> set:
    """
    Context-Free Path Querying based on Hellings Algorithm

    Parameters
    ----------
    graph: MultiDiGraph
        Labeled graph for the Path Querying task
    cfg: CFG
        Query given in Context Free Grammar form
    start_nodes: set, default=None
        Set of graph start nodes
    final_nodes: set, default=None
        Set of graph final nodes
    start_var: Variable, default=Variable("S")
        Start variable of a grammar

    Returns
    -------
    cfpq: set
        Context Free Path Querying
    """
    cfg._start_symbol = start_var
    wcnf = transform_cfg_to_wcnf(cfg)
    reach_pairs = {
        (u, v) for u, h, v in hellings(wcnf, graph) if h == wcnf.start_symbol.value
    }
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs
