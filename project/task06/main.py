from pyformlang.cfg import CFG, Variable, Terminal, Epsilon


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    return CFG(
        start_symbol=cfg.start_symbol,
        productions=cfg._decompose_productions(
            cfg._get_productions_with_only_single_terminals()
        ),
    )


# https://jhellings.nl/files/icdt2014_paper.pdf
def cfpq_with_hellings(
    cfg,
    graph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    start_nodes = graph.nodes if start_nodes is None else start_nodes
    final_nodes = graph.nodes if final_nodes is None else final_nodes

    P_terminal = {}
    P_epsilon = set()
    P_mult = {}

    for p in cfg_to_weak_normal_form(cfg).productions:
        if len(p.body) == 0:
            P_epsilon.add(p.head)
        elif len(p.body) == 1 and isinstance(p.body[0], Terminal):
            P_terminal.setdefault(p.head, set()).add(p.body[0])
        elif len(p.body) == 2:
            P_mult.setdefault(p.head, set()).add((p.body[0], p.body[1]))

    r = {(N, n, n) for N in P_epsilon for n in graph.nodes} | {
        (N, n, m)
        for (n, m, tag) in graph.edges.data("label")
        for N in P_terminal
        if Terminal(tag) in P_terminal[N]
    }

    new = r.copy()

    while new:
        N, n, m = new.pop()
        to_add = set()
        for M, np, n_ in r:
            if n == n_:
                for Np in P_mult:
                    if (M, N) in P_mult[Np]:
                        if (Np, np, m) not in r:
                            new.add((Np, np, m))
                            to_add.add((Np, np, m))

        for M, m_, mp in r:
            if m == m_:
                for Mp in P_mult:
                    if (N, M) in P_mult[Mp]:
                        if (Mp, n, mp) not in r:
                            new.add((Mp, n, mp))
                            to_add.add((Mp, n, mp))
        r |= to_add

    return {
        (n, m)
        for (N, n, m) in r
        if n in start_nodes and m in final_nodes and Variable(N) == cfg.start_symbol
    }
