import scipy
from pyformlang.cfg import Variable, Epsilon
from typing import Tuple
from scipy.sparse import csr_matrix
from project.task06 import cfg_to_weak_normal_form


def cfpq_with_matrix(
    cfg,
    graph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[Tuple[int, int]]:

    cfg = cfg_to_weak_normal_form(cfg)
    n = len(graph.nodes)
    products = {var: csr_matrix((n, n), dtype=bool) for var in cfg.variables}

    P_mult = set()

    for i, j, tag in graph.edges.data("label"):
        for p in cfg.productions:
            if len(p.body) == 1:
                if isinstance(p.body[0], Variable) and p.body[0].value == tag:
                    products[p.head][i, j] = True
                elif isinstance(p.body[0], Epsilon):
                    products[p.head] += csr_matrix(scipy.eye(n), dtype=bool)
            elif len(p.body) == 2:
                P_mult.add((p.head, p.body[0], p.body[1]))

    r = {i: v for i, v in enumerate(graph.nodes)}
    products = {Np: csr_matrix(m) for (Np, m) in products.items()}

    new = True
    while new:
        new = False
        for Np, M, N in P_mult:
            prev = products[Np].nnz
            products[Np] += products[M] @ products[N]
            new |= prev != products[Np].nnz

    return {(r[m], r[n]) for _, M in products.items() for m, n in zip(*M.nonzero())}
