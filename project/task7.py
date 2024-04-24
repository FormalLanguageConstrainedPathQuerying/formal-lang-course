from pyformlang.cfg import CFG, Variable, Terminal
import pyformlang
import networkx as nx
from typing import *
from scipy.sparse import dok_matrix


def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
    elimUnit = cfg.eliminate_unit_productions()
    elimUnitUseless = elimUnit.remove_useless_symbols()
    productions = elimUnitUseless._decompose_productions(
        elimUnitUseless._get_productions_with_only_single_terminals()
    )
    return CFG(productions=set(productions), start_symbol=Variable("S"))


def cfpq_with_matrix(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    cfg = cfg.to_normal_form()
    n = len(graph.nodes)
    r = {}

    for i, j, data in graph.edges(data=True):
        label = data["label"]
        for production in cfg.productions:
            if (
                len(production.body) == 1
                and isinstance(production.body[0], Variable)
                and production.body[0].value == label
            ):
                if (i, j) not in r:
                    r[(i, j)] = set()
                r[(i, j)].add(production.head)

    changes = True
    while changes:
        changes = False
        new_r = r.copy()
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if (i, k) in r and (k, j) in r:
                        for production in cfg.productions:
                            if len(production.body) == 2:
                                B, C = production.body
                                if B in r[(i, k)] and C in r[(k, j)]:
                                    if (i, j) not in new_r:
                                        new_r[(i, j)] = set()
                                    if production.head not in new_r[(i, j)]:
                                        new_r[(i, j)].add(production.head)
                                        changes = True
        r = new_r

    result = set()
    for i in range(n):
        for j in range(n):
            if (i, j) in r:
                if (start_nodes is None or i in start_nodes) and (
                    final_nodes is None or j in final_nodes
                ):
                    result.add((i, j))

    return result
