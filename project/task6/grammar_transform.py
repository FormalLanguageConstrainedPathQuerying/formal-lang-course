from typing import Set, Tuple
import pyformlang
from pyformlang.cfg import Terminal, Epsilon
from pyformlang.cfg.cfg import CFG, Variable
import networkx as nx


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg_update = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_prod = cfg_update._decompose_productions(
        cfg_update._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=cfg_update.start_symbol, productions=new_prod)


def cfg_from_file(path: str) -> CFG:
    with open(path) as f:
        return CFG.from_text(f.read())


def cfpq_with_hellings(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    g = cfg_to_weak_normal_form(cfg)
    p1 = {}
    p2 = set()
    p3 = {}

    for p in g.productions:
        if len(p.body) == 1 and isinstance(p.body[0], Terminal):
            p1.setdefault(p.head, set()).add(p.body[0])
        elif len(p.body) == 1 and isinstance(p.body[0], Epsilon):
            p2.add(p.body[0])
        elif len(p.body) == 2:
            p3.setdefault(p.head, set()).add((p.body[0], p.body[1]))

    r = {(N_i, v, v) for N_i in p2 for v in graph.nodes}
    r |= {
        (N_i, v, u)
        for (v, u, tag) in graph.edges.data("label")
        for N_i in p1
        if tag in p1[N_i]
    }

    m = r.copy()

    while len(m) > 0:
        N_i, v, u = m.pop()

        r_tmp = set()
        for N_j, v_, u_ in r:
            if v == u_:
                for N_k in p3:
                    if (N_j, N_i) in p3[N_k] and (N_k, v_, v) not in r:
                        m.add((N_k, v_, u))
                        r_tmp.add((N_k, v_, u))
        r |= r_tmp

    return {
        (v, u)
        for (N_i, v, u) in r
        if v in start_nodes and u in final_nodes and Variable(N_i) == cfg.start_symbol
    }
