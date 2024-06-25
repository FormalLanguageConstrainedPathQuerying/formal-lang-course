from typing import Set, Tuple
import pyformlang
from pyformlang.cfg import Terminal, Epsilon
from pyformlang.cfg.cfg import CFG, Variable
import networkx as nx


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    tmp = cfg._get_productions_with_only_single_terminals()
    new_prod = cfg._decompose_productions(tmp)
    return CFG(start_symbol=cfg.start_symbol, productions=new_prod)


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

    cfg = cfg_to_weak_normal_form(cfg)
    eps = set()
    terms = {}
    nn = {}

    for p in cfg.productions:
        if len(p.body) == 0:
            eps.add(p.head)
        if len(p.body) == 1 and isinstance(p.body[0], Terminal):
            terms.setdefault(p.head, set()).add(p.body[0])
        elif len(p.body) == 2:
            nn.setdefault(p.head, set()).add((p.body[0], p.body[1]))

    r = {(N, v, v) for N in eps for v in graph.nodes}
    r |= {
        (N, v, u)
        for N, ls in terms.items()
        for v, u, tag in graph.edges(data="label")
        if Terminal(tag) in ls
    }

    m = r.copy()

    while len(m) > 0:
        N_i, v, u = m.pop()
        r_tmp = set()
        for N_j, v_, u_ in r:
            if v == u_:
                for N_k, NNs in nn.items():
                    if (N_j, N_i) in NNs and (N_k, v_, u) not in r:
                        m.add((N_k, v_, u))
                        r_tmp.add((N_k, v_, u))
            if v_ == u:
                for M_k, NNs in nn.items():
                    if (N_i, N_j) in NNs and (M_k, v, u_) not in r:
                        m.add((M_k, v, u_))
                        r_tmp.add((M_k, v, u_))
        r |= r_tmp

    return {
        (v, u)
        for N_i, v, u in r
        if v in start_nodes and u in final_nodes and N_i == cfg.start_symbol
    }
