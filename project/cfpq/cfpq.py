from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from typing import Set, Tuple, Callable

from project.grammars.hellings import hellings
from project.grammars.matrix_based import matrix_based
from project.utils.CFG_utils import transform_cfg_to_wcnf, is_wcnf


__all__ = ["cfpq_hellings", "cfpq_matrix"]


def _filter_pairs(
    pairs: Set[Tuple[int, int]],
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Filter pairs.
    Keep pairs where first node in start nodes and second node in final nodes

    Parameters
    ----------
    pairs: Set[Tuple[int, int]]
        Pairs obtained from cfpq algorithm
    start_nodes: Set[int], default = None
        Start nodes
    final_nodes: Set[int], default = None
        Final nodes

    Returns
    -------
    filtered_pairs: Set[Tuple[int, int]]
        Filtered pairs according to start and final nodes
    """
    if start_nodes:
        pairs = {(u, v) for u, v in pairs if u in start_nodes}
    if final_nodes:
        pairs = {(u, v) for u, v in pairs if v in final_nodes}

    return pairs


def _cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
    algorithm: Callable = hellings,
) -> Set[Tuple[int, int]]:
    """
    Context-Free Path Querying function
    Available algorithms:
        1. hellings
        2. matrix_based
        3. [WIP] tensor

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
    cfpq: Set[Tuple[int, int]]
        Context Free Path Querying
    """

    cfg._start_symbol = start_var
    wcnf = cfg if is_wcnf(cfg) else transform_cfg_to_wcnf(cfg)
    reach_pairs = {
        (u, v) for u, h, v in algorithm(wcnf, graph) if h == wcnf.start_symbol
    }

    return _filter_pairs(reach_pairs, start_nodes, final_nodes)


def cfpq_hellings(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """
    Context-Free Path Querying based on Hellings Algorithm

    Parameters
    ----------
    graph: MultiDiGraph
        Labeled graph for the Path Querying task
    cfg: CFG
        Query given in Context Free Grammar form
    start_nodes: Set[int], default=None
        Set of graph start nodes
    final_nodes: Set[int], default=None
        Set of graph final nodes
    start_var: Variable, default=Variable("S")
        Start variable of a grammar

    Returns
    -------
    cfpq: Set[Tuple[int, int]]
        Context Free Path Querying
    """
    return _cfpq(graph, cfg, start_nodes, final_nodes, start_var, algorithm=hellings)


def cfpq_matrix(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """
    Context-Free Path Querying based on Matrix Multiplication

    Parameters
    ----------
    graph: MultiDiGraph
        Labeled graph for the Path Querying task
    cfg: CFG
        Query given in Context Free Grammar form
    start_nodes: Set[int], default=None
        Set of graph start nodes
    final_nodes: Set[int], default=None
        Set of graph final nodes
    start_var: Variable, default=Variable("S")
        Start variable of a grammar

    Returns
    -------
    cfpq: Set[Tuple[int, int]]
        Context Free Path Querying
    """
    return _cfpq(
        graph, cfg, start_nodes, final_nodes, start_var, algorithm=matrix_based
    )
