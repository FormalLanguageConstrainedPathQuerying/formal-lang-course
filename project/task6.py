import networkx as nx

from pyformlang.cfg import CFG


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()

    production_with_single_terminal = cfg._get_productions_with_only_single_terminals()

    new_productions = set(cfg._decompose_productions(production_with_single_terminal))

    return CFG(start_symbol=cfg.start_symbol, productions=new_productions)


def hellings_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    weak_normal_form = cfg_to_weak_normal_form(cfg)
    result = set()

    null_vars = weak_normal_form.get_nullable_symbols()
    for var in null_vars:
        for node in graph.nodes:
            result.add((node, var, node))

    for n, m, data in graph.edges(data=True):
        label = data.get("label")
        if label is None:
            continue
        for production in weak_normal_form.productions:
            if len(production.body) == 1:
                if label == production.body[0].value:
                    result.add((n, production.head, m))

    found = True
    while found:
        found = False
        new_results = set()

        for start_node_1, headvar_1, end_node_1 in result:
            for start_node_2, headvar_2, end_node_2 in result:
                if end_node_1 == start_node_2:
                    for production in weak_normal_form.productions:
                        if len(production.body) == 2:
                            if (production.body[0] == headvar_1) & (
                                production.body[1] == headvar_2
                            ):
                                triple_production = (
                                    start_node_1,
                                    production.head,
                                    end_node_2,
                                )
                                if triple_production not in result:
                                    new_results.add(triple_production)
                                    found = True

        result.update(new_results)

    result_pairs = set()
    for start, var, final in result:
        if var != weak_normal_form.start_symbol:
            continue
        if (var == cfg.start_symbol) & (start in start_nodes) & (final in final_nodes):
            result_pairs.add((start, final))

    return result_pairs
