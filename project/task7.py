import copy

from pyformlang.cfg import Variable

from typing import Set
import networkx as nx
import pyformlang

from project.task6 import cfg_to_weak_normal_form


def cfpq_with_matrix(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    grammatics = cfg_to_weak_normal_form(cfg)
    n = graph.number_of_nodes()
    met_init = {}

    for i, j, data in graph.edges(data=True):
        for production in grammatics.productions:
            if (
                len(production.body) == 1
                and isinstance(production.body[0], Variable)
                and production.body[0].value == data["label"]
            ):
                if (i, j) not in met_init:
                    met_init[(i, j)] = set()
                met_init[(i, j)].add(production.head)

    _met = copy.deepcopy(met_init)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if (i, k) in met_init and (k, j) in met_init:
                    for production in grammatics.productions:

                        if len(production.body) == 2:
                            mat_b, mat_c = production.body
                            if mat_b in met_init[(i, k)] and mat_c in met_init[(k, j)]:
                                if (i, j) not in _met:
                                    _met[(i, j)] = set()
                                if production.head not in _met[(i, j)]:
                                    _met[(i, j)].add(production.head)
        met_init = _met

    res = set()

    for i in range(n):
        for j in range(n):
            if (i, j) in met_init:
                if (start_nodes is None or i in start_nodes) and (
                    final_nodes is None or j in final_nodes
                ):
                    res.add((i, j))

    return res
