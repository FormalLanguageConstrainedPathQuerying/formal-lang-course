import networkx as nx
from scipy.sparse import dok_matrix

from pyformlang.cfg import CFG, Variable
from project.cfg import cfg_to_wcnf, is_wcnf


def matrix_alg(
    graph: nx.MultiDiGraph, cfg: CFG
) -> set[tuple[int, str, int]]:  # (node, nonterminal, node)
    wcnf = cfg if is_wcnf(cfg) else cfg_to_wcnf(cfg)

    eps_prod_heads = [
        production.head.value for production in wcnf.productions if not production.body
    ]
    term_productions = {
        production for production in wcnf.productions if len(production.body) == 1
    }
    var_productions = {
        production for production in wcnf.productions if len(production.body) == 2
    }
    nodes_number = graph.number_of_nodes()
    matrices = {
        v.value: dok_matrix((nodes_number, nodes_number), dtype=bool)
        for v in wcnf.variables
    }

    for i, j, data in graph.edges(data=True):
        l = data["label"]
        for v in {
            production.head.value
            for production in term_productions
            if production.body[0].value == l
        }:
            matrices[v][i, j] = True

    for i in range(nodes_number):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    any_changing = True
    while any_changing:
        any_changing = False
        for production in var_productions:
            old_nnz = matrices[production.head.value].nnz
            matrices[production.head.value] += (
                matrices[production.body[0].value] @ matrices[production.body[1].value]
            )
            new_nnz = matrices[production.head.value].nnz
            any_changing = any_changing or (old_nnz != new_nnz)

    return {
        (u, var, v) for var in wcnf.variables for u, v in zip(*matrices[var].nonzero())
    }


def matrix_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[tuple[int, int]]:
    cfg._start_symbol = start_var
    wcnf = cfg_to_wcnf(cfg)
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    return {
        (u, v)
        for u, var, v in matrix_alg(graph, wcnf)
        if var == wcnf.start_symbol.value and u in start_nodes and v in final_nodes
    }
