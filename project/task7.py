import itertools
from typing import Tuple
import numpy as np
from pyformlang.cfg import CFG, Terminal, Epsilon, Variable
import networkx as nx
from scipy.sparse import csr_matrix


from project.task6 import cfg_to_weak_normal_form


def matrix_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    weak_normal_form = cfg_to_weak_normal_form(cfg)

    term_productions: dict[Terminal, set[Variable]] = {}
    eps_productions: set[Variable] = set()
    nonterms_productions: dict[Tuple[Variable, Variable], set[Variable]] = {}

    for production in weak_normal_form.productions:
        head = production.head
        body = production.body
        if len(body) == 1 and isinstance(body[0], Terminal):
            prods = term_productions.setdefault(body[0].value, set())
        elif len(body) == 0 or isinstance(body[0], Epsilon):
            prods = eps_productions
        else:
            prods = nonterms_productions.setdefault((body[0], body[1]), set())
        prods.add(head)

    index_of_nodes = {n: i for i, n in enumerate(graph.nodes)}
    n = len(graph.nodes)
    adjacency_matrices = {
        var: csr_matrix((n, n), dtype=np.bool_) for var in weak_normal_form.variables
    }
    for u, v, label in graph.edges(data="label"):
        if label in term_productions:
            for terminal in term_productions[label]:
                adjacency_matrices[terminal][index_of_nodes[u], index_of_nodes[v]] = (
                    True
                )

    for production in eps_productions:
        for i in range(n):
            adjacency_matrices[production][i, i] = True

    queue = set(weak_normal_form.variables)
    while queue:
        updated_var = queue.pop()
        for (B, C), variables in nonterms_productions.items():
            if not (updated_var == B or updated_var == C):
                continue
            new_vars = adjacency_matrices[B] @ adjacency_matrices[C]
            for variable in variables:
                before = adjacency_matrices[variable]
                adjacency_matrices[variable] += new_vars
                if (before - adjacency_matrices[variable]).count_nonzero() > 0:
                    queue.add(variable)
    res = set()
    adjacency_matrix = adjacency_matrices[weak_normal_form.start_symbol]
    for start_node, final_node in itertools.product(start_nodes, final_nodes):
        if adjacency_matrix[index_of_nodes[start_node], index_of_nodes[final_node]]:
            res.add((start_node, final_node))
    return res
