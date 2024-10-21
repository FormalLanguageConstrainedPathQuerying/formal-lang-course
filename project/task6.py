from pyformlang.cfg import CFG, Terminal, Production
from networkx import DiGraph
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

    lam = wcnf.get_nullable_symbols()  # λ

    for n in graph.nodes:
        for N in lam:
            res.append((N, n, n))  # {(N, n, n) | N -> λ}

    for n, m, label in graph.edges.data("label"):
        if label is None:
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

        (N, n, m) = new.pop()

        # (M, n', n)
        for M, x, n_ in res:
            if n_ != n:
                continue

            for prod in wcnf.productions:
                body = prod.body
                head = prod.head

                el = (head, x, m)

                # N' -> M and (N', n', m) not in r
                if (len(body) == 2 and body[0].value == M and body[1] == N) and (
                    (el not in res) and (el not in new)
                ):
                    new.append(el)
                    res.append(el)

        # (M, m, m')
        for M, m_, y in res:
            if m_ != m:
                continue

            for prod in wcnf.productions:
                body = prod.body
                head = prod.head

                el = (head, n, y)

                # (M_ -> N) and ((M_, n, m_) not in res)
                if (len(body) == 2 and body[0].value == N and body[1] == M) and (
                    (el not in res) and (el not in new)
                ):
                    new.append(el)
                    res.append(el)

    res = set(res)
    pairs: set[tuple[int, int]] = set()
    start = graph.nodes if start_nodes is None else start_nodes
    final = graph.nodes if final_nodes is None else final_nodes

    for N, n, m in res:
        if (N == wcnf.start_symbol) and (n in start) and (m in final):
            pairs.add((n, m))

    return pairs
