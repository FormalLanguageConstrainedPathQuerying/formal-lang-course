import networkx as nx

from pyformlang.cfg import CFG, Variable
from project.cfg import cfg_to_wcnf, is_wcnf


def hellings_alg(
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

    r = {
        (node, var, node)
        for node in range(graph.number_of_nodes())
        for var in eps_prod_heads
    } | {
        (u, production.head.value, v)
        for u, v, edge_data in graph.edges(data=True)
        for production in term_productions
        if production.body[0].value == edge_data["label"]
    }

    new = r.copy()
    while new:
        n, N, m = new.pop()
        tmp_set = (
            set()
        )  # Otherwise, size of set r will change during iteration -- this is prohibited

        for u, M, v in r:
            if v == n:
                triplets = {
                    (u, production.head.value, m)
                    for production in var_productions
                    if production.body[0].value == M
                    and production.body[1].value == N
                    and (u, production.head.value, m) not in r
                }
                new |= triplets
                tmp_set |= triplets
        r |= tmp_set
        tmp_set.clear()

        for u, M, v in r:
            if u == m:
                triplets = {
                    (n, production.head.value, v)
                    for production in var_productions
                    if production.body[0].value == N
                    and production.body[1].value == M
                    and (n, production.head.value, v) not in r
                }
                new |= triplets
                tmp_set |= triplets
        r |= tmp_set

    return r


def hellings_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_variable: Variable = Variable("S"),
) -> set[tuple[int, int]]:
    cfg._start_symbol = start_variable
    wcnf = cfg_to_wcnf(cfg)
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    return {
        (u, v)
        for u, var, v in hellings_alg(graph, wcnf)
        if var == wcnf.start_symbol.value and u in start_nodes and v in final_nodes
    }
