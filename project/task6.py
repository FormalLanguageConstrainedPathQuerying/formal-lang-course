from symtable import Symbol
from numpy import isin
from pyformlang.cfg import CFG, Variable, Terminal, Production
from networkx import DiGraph
from itertools import product
from typing import Tuple


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    null_syms = cfg.get_nullable_symbols()
    norm_productions: set[Production] = set(cfg.to_normal_form().productions)

    # return back the ability to product epsilons from the non-terminals
    for sym in null_syms:
        norm_productions.add(Production(sym, []))

    new_cfg = CFG(cfg.variables, cfg.terminals, cfg.start_symbol, norm_productions)

    return new_cfg


def hellings_based_cfpq(
    cfg: CFG,
    graph: DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    wcnf = cfg_to_weak_normal_form(cfg)  # G
    res: list[Tuple[Production, int, int]] = []  # r

    edges = list(graph.edges)
    nodes = list(graph.nodes)

    lam = wcnf.get_nullable_symbols()  # λ

    for n in nodes:
        for N in lam:
            res.append((N, n, n))  # {(N, n, n) | N -> λ}

    for n, m, _ in edges:
        label = graph.get_edge_data(n, m)[0]["label"]  # l
        if not label:
            continue

        for prod in wcnf.productions:
            head = prod.head  # N
            body = prod.body  # N -> ...

            # if right part of production contains only 1 sym
            if (
                len(body) == 1
                and isinstance(body[0], Terminal)
                and body[0].value == label
            ):
                res.append((head, n, m))  # r = {(N, n, m) | ...}

    new = res.copy()

    while len(new) > 0:
        # pick and remove a (N, n, m)
        (N, n, m) = new.pop(0)

        # (M, n', n)
        for M, k, p in res:
            if p != n:
                continue

            for prod in wcnf.productions:
                body = prod.body
                head = prod.head

                el = (head, k, m)

                # N' -> M and (N', n', m) not in r
                if (len(body) == 2 and body[0].value == M and body[1] == N) and (
                    el not in res
                ):
                    new.append(el)
                    res.append(el)

        for M, k, p in res:
            if k != m:
                continue

            for prod in wcnf.productions:
                body = prod.body
                head = prod.head

                el = (head, m, p)

                # (M_ -> N) and ((M_, n, m_) not in res)
                if (len(body) == 2 and body[0].value == N and body[1] == M) and (
                    el not in res
                ):
                    new.append(el)
                    res.append(el)

    pairs: set[tuple[int, int]] = set()
    start_nodes = graph.nodes if not start_nodes else start_nodes
    final_nodes = graph.nodes if not start_nodes else start_nodes

    for N, n, m in res:
        if (N == wcnf.start_symbol) and (n in start_nodes) and (m in final_nodes):
            pairs.add((n, m))

    return pairs


var_useless = Variable("USELESS")
var_S = Variable("S")
var_B = Variable("B")

# Creation of terminals
ter_a = Terminal("a")
ter_b = Terminal("b")
ter_c = Terminal("c")

# Creation of productions
p0 = Production(var_S, [ter_a, var_S, var_B])
p1 = Production(var_useless, [ter_a, var_S, var_B])
p2 = Production(var_S, [var_useless])
p4 = Production(var_B, [ter_b])
p5 = Production(var_useless, [])

# Creation of the CFG
cfg = CFG({var_useless, var_S}, {ter_a, ter_b}, var_S, {p0, p1, p2, p4, p5})
