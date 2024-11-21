import networkx as nx
from pyformlang.cfg import CFG, Variable, Production, Epsilon
import itertools


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
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
    nullable = weak_normal_form.get_nullable_symbols()

    cfpq_results = set()

    for u, v, label in graph.edges(data="label"):
        for prod in weak_normal_form.productions:
            if len(prod.body) == 1 and (prod.body[0].value == label):
                cfpq_results.add((u, prod.head, v))

    for node in graph.nodes:
        for var in nullable:
            cfpq_results.add((node, var, node))

    added = True
    while added:
        added = False
        new_results = set()

        for (u1, var1, u2), (u1_, var2, u2_) in itertools.product(
            cfpq_results, repeat=2
        ):
            if u2 == u1_:
                for prod in weak_normal_form.productions:
                    if (
                        len(prod.body) == 2
                        and prod.body[0] == var1
                        and prod.body[1] == var2
                        and (new_triple := (u1, prod.head, u2_)) not in cfpq_results
                    ):
                        new_results.add(new_triple)
                        added = True

        cfpq_results.update(new_results)

    result_pairs = set()
    for u, var, v in cfpq_results:
        if var == weak_normal_form.start_symbol:
            if u in start_nodes:
                if v in final_nodes:
                    result_pairs.add((u, v))

    return result_pairs
