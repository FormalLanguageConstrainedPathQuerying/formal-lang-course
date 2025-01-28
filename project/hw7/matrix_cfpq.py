from itertools import product
from typing import Any, Set

import networkx as nx
import pyformlang
import scipy as sp
from project.hw6.cfg_to_weak_normal_form import cfg_to_weak_normal_form


def matrix_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    wcnf_cfg = cfg_to_weak_normal_form(cfg)
    from_term_to_nterm = {}
    from_nterm_to_body = {}
    for production in wcnf_cfg.productions:
        if len(production.body) == 2:
            from_nterm_to_body.setdefault(tuple(production.body), set()).add(
                production.head
            )

        if len(production.body) == 1 and isinstance(
            production.body[0], pyformlang.cfg.Terminal
        ):
            from_term_to_nterm.setdefault(production.body[0], set()).add(
                production.head
            )

    g_size = graph.number_of_nodes()
    idx_to_node = {i: node for i, node in enumerate(graph.nodes)}
    node_to_idx = {node: i for i, node in idx_to_node.items()}

    bool_decompose_matrices: dict[Any, sp.sparse.csc_matrix] = {
        var: sp.sparse.csc_matrix((g_size, g_size), dtype=bool)
        for var in wcnf_cfg.variables
    }

    for v1, v2, lb in graph.edges.data("label"):
        term_vars = from_term_to_nterm.get(pyformlang.cfg.Terminal(lb), set())
        idx1, idx2 = node_to_idx[v1], node_to_idx[v2]
        for var in term_vars:
            bool_decompose_matrices[var][idx1, idx2] = True

    for v, var in product(graph.nodes, wcnf_cfg.get_nullable_symbols()):
        idx = node_to_idx[v]
        bool_decompose_matrices[var][idx, idx] = True

    recently_updated = list(wcnf_cfg.variables)
    while recently_updated:
        updated_var = recently_updated.pop(0)
        for body, heads in from_nterm_to_body.items():
            if updated_var not in body:
                continue

            new_matrix: sp.sparse.csc_matrix = (
                bool_decompose_matrices[body[0]] @ bool_decompose_matrices[body[1]]
            )
            for head in heads:
                old_matrix = bool_decompose_matrices[head]
                bool_decompose_matrices[head] += new_matrix
                if (old_matrix != bool_decompose_matrices[head]).count_nonzero():
                    recently_updated.append(head)

    start_var = wcnf_cfg.start_symbol
    if start_var not in bool_decompose_matrices:
        return set()

    return {
        (idx_to_node[idx1], idx_to_node[idx2])
        for idx1, idx2 in zip(*bool_decompose_matrices[start_var].nonzero())
        if idx_to_node[idx1] in start_nodes and idx_to_node[idx2] in final_nodes
    }
