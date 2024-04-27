from pyformlang.cfg import CFG, Variable, Terminal
import pyformlang
import networkx as nx
from typing import *
from scipy.sparse import dok_matrix
from project.task6 import cfg_to_weak_normal_form


def cfpq_with_matrix(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    cfg = cfg.to_normal_form()
    n = len(graph.nodes)
    r = dok_matrix((n, n), dtype=bool)

    for i, j, data in graph.edges(data=True):
        label = data["label"]
        for production in cfg.productions:
            if (
                len(production.body) == 1
                and isinstance(production.body[0], Variable)
                and production.body[0].value == label
            ):
                r[i, j] = True

    changes = True
    while changes:
        changes = False
        new_r = r.copy()
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if r[i, k] and r[k, j]:
                        for production in cfg.productions:
                            if len(production.body) == 2:
                                B, C = production.body
                                if B.value in r[i, k] and C.value in r[k, j]:
                                    if not new_r[i, j]:
                                        new_r[i, j] = True
                                        changes = True
        r = new_r

    result = set()
    for i in range(n):
        for j in range(n):
            if r[i, j]:
                if (start_nodes is None or i in start_nodes) and (
                    final_nodes is None or j in final_nodes
                ):
                    result.add((i, j))

    return result
