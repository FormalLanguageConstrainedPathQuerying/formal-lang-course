from pyformlang.cfg import CFG, Epsilon, Terminal, Variable
from networkx import MultiDiGraph
from project.cfg_utils import cfg2wcnf, from_file
import pathlib
from typing import List


def hellings(graph: MultiDiGraph, cfg):
    """
    Perform Hellings reachability algorithm

    Args:
        graph: graph (any type from networkx.Graph)
        cfg: context free grammar as file or pyformlang CFG

    Returns:
        set of triplet tuples of starting graph node, CFG variable, final achievable graph node
    """

    if not isinstance(cfg, CFG):
        cfg = from_file(cfg)

    cfg = cfg2wcnf(cfg)

    res = set()

    for prod in cfg.productions:
        if len(prod.body) == 0:
            [res.add((node, prod.head, node)) for node in graph.nodes]
        elif len(prod.body) == 1:
            [
                res.add((u, prod.head, v))
                for u, v, label in graph.edges.data(data="label")
                if Variable(label) == prod.body[0]
            ]

    queue = list(res)

    while len(queue) > 0:
        u1, var1, v1 = queue.pop()

        next_res = set()

        for u2, var2, v2 in res:
            if v2 != u1:
                continue

            for prod in cfg.productions:
                if prod.body == [var2, var1] and (u2, prod.head, v1) not in res:
                    next_res.add((u2, prod.head, v1))

        for v2, var2, u2 in res:
            if v2 != v1:
                continue

            for prod in cfg.productions:
                if prod.body == [var1, var2] and (u1, prod.head, u2) not in res:
                    next_res.add((u1, prod.head, u2))

        [res.add(t) for t in next_res]
        [queue.append(t) for t in next_res]

    return res


def hellings_context_free_path_query(
    graph: MultiDiGraph,
    cfg: CFG,
    start_states: List[any] = None,
    final_states: List[any] = None,
    nonterm: Variable = None,
):
    """
    Queries given graph reachability problem for a given set of start and end ndoes,
    and a given nonterminal using the Hellings algorithm

    Args:
        graph: the graph to query
        cfg: context-free grammar
        start_states: start nodes of the given graph
        final_states: final nodes of the given graph
        nonterm: nonterminal

    Returns:
        set of node pairs
    """
    if start_states is None:
        start_states = set(graph.nodes)

    if final_states is None:
        final_states = set(graph.nodes)

    if nonterm is None:
        nonterm = cfg.start_symbol

    return {
        (v, u)
        for v, n, u in hellings(graph, cfg)
        if n == nonterm and v in start_states and u in final_states
    }
