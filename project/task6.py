from symtable import Symbol
from pyformlang.cfg import CFG, Variable, Terminal, Production
from networkx import DiGraph
from itertools import product


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
    res = set()  # r

    edges = list(graph.edges)
    nodes = list(graph.nodes)

    lam = wcnf.get_nullable_symbols()  # λ
    for n, N in product(nodes, lam):
        res.add((N, n, n))  # {(N, n, n) | ...}

    for n, m, prod in product(edges, wcnf.productions):
        head = prod.head  # N
        body = prod.body  # N -> ...
        label = graph.get_edge_data(n, m)[0]["data"]  # l

        # if right part of production contains only 1 sym
        if len(body) == 1 and isinstance(body[0], Terminal) and body[0].value == label:
            res.add((head, n, m))  # r = {(N, n, m) | ...}

    new_res = res.copy()

    while len(new_res) > 0:
        # (M, n', n)
        for M, n_, n in res:
            # (N', m', m)
            for N_, m_, m in res:
                for prod in wcnf.productions:
                    body = prod.body
                    head = prod.head

                    # N' -> M and (N', n', m) not in r
                    if (len(body) == 1 and head == N_ and body[0] == M) and (
                        (N_, n_, m) not in res
                    ):
                        new_res.union((N_, n_, m))  # res union (N', n', m)
                        res.union(new_res)

        for M, m, m_ in res:
            for N_, n_, n in res:
                for prod in wcnf.productions:
                    body = prod.body
                    head = prod.head

                    if (len(body) == 1 and head == M and body[0] == N_) and (
                        (M, n, m_) not in res
                    ):
                        new_res = new_res.union((M, n, m))
                        res = res.union(new_res)

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
