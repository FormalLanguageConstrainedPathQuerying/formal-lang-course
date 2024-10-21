from pyformlang.cfg import CFG, Production, Variable, Epsilon
import networkx as nx


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    if len(cfg.productions) == 0:
        return cfg

    normal_form_cfg = cfg.to_normal_form()
    nullable = cfg.get_nullable_symbols()

    new_productions = set(normal_form_cfg.productions)
    for var in nullable:
        new_productions.add(Production(Variable(var.value), [Epsilon()]))

    return CFG(
        start_symbol=cfg.start_symbol, productions=new_productions
    ).remove_useless_symbols()


def hellings_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    weak_normal_form = cfg_to_weak_normal_form(cfg)

    transitions = set()

    for u, v, label in graph.edges(data="label"):
        for production in weak_normal_form.productions:
            if len(production.body) == 1 and production.body[0].value == label:
                transitions.add((u, production.head, v))

    nullable = weak_normal_form.get_nullable_symbols()
    for node in graph.nodes:
        for label in nullable:
            transitions.add((node, label, node))

    added = True
    while added:
        added = False
        delta = set()

        for from_1, N1, to_1 in transitions:
            for from_2, N2, to_2 in transitions:
                if to_1 == from_2:
                    for production in weak_normal_form.productions:
                        if (
                            len(production.body) == 2
                            and production.body[0] == N1
                            and production.body[1] == N2
                        ):
                            new_triple = (from_1, production.head, to_2)
                            if new_triple not in transitions:
                                delta.add(new_triple)
                                added = True
        transitions.update(delta)

    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    res = set()
    for u, label, v in transitions:
        if label == weak_normal_form.start_symbol:
            if (u in start_nodes) and (v in final_nodes):
                res.add((u, v))

    return res
