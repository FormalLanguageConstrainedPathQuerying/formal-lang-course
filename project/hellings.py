import networkx as nx
import pyformlang.cfg as c
from typing import Set, Tuple

from project.cfg import cfg_to_wcnf


def hellings(graph: nx.Graph, cfg: c.CFG) -> Set[Tuple[int, str, int]]:
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}

    r = {(v, h, v) for v in range(graph.number_of_nodes()) for h in eps_prod_heads} | {
        (u, p.head.value, v)
        for u, v, edge_data in graph.edges(data=True)
        for p in term_productions
        if p.body[0].value == edge_data["label"]
    }

    new = r.copy()
    while new:
        n, N, m = new.pop()
        r_temp = set()

        for u, M, v in r:
            if v == n:
                triplets = {
                    (u, p.head.value, m)
                    for p in var_productions
                    if p.body[0].value == M
                    and p.body[1].value == N
                    and (u, p.head.value, m) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp
        r_temp.clear()

        for u, M, v in r:
            if u == m:
                triplets = {
                    (n, p.head.value, v)
                    for p in var_productions
                    if p.body[0].value == N
                    and p.body[1].value == M
                    and (n, p.head.value, v) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp

    return r


def cfpq_by_hellings(
    graph: nx.Graph,
    query: str | c.CFG,
    start_nodes: set[int] | None = None,
    final_nodes: set[int] | None = None,
    start_var: str | c.Variable = c.Variable("S"),
) -> set[tuple[int, int]]:
    if not isinstance(start_var, c.Variable):
        start_var = c.Variable(start_var)
    if not isinstance(query, c.CFG):
        query = c.CFG.from_text(query, start_symbol=start_var)
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    if start_var is None:
        start_var = query.start_symbol

    constrained_transitive_closure = hellings(graph, query)

    return {
        (start, final)
        for start, var, final in constrained_transitive_closure
        if start in start_nodes and var == start_var and final in final_nodes
    }
