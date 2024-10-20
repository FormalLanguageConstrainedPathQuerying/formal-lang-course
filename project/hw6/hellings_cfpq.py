import pyformlang
import networkx as nx
from project.hw6.cfg_to_weak_normal_form import cfg_to_weak_normal_form
from pyformlang.cfg import Terminal


def hellings_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    wcnf_cfg = cfg_to_weak_normal_form(cfg)
    adj_set = set()
    for start, end, data in graph.edges(data=True):
        label_ = data.get("label")
        if label_ is not None:
            for prod in wcnf_cfg.productions:
                if len(prod.body) == 1 and isinstance(prod.body[0], Terminal):
                    term = prod.body[0].value
                    if term == label_:
                        adj_set.add((start, prod.head, end))

    eps_els = wcnf_cfg.get_nullable_symbols()
    for el in graph.nodes:
        for el1 in eps_els:
            adj_set.add((el, el1, el))

    updated = True
    while updated:
        updated = False
        new_edges = set()

        for node1, label1, node2 in adj_set:
            for node3, label2, node4 in adj_set:
                if node2 == node3:
                    for prod in wcnf_cfg.productions:
                        if (
                            len(prod.body) == 2
                            and prod.body[0] == label1
                            and prod.body[1] == label2
                        ):
                            new_edge = (node1, prod.head, node4)
                            if new_edge not in adj_set:
                                new_edges.add(new_edge)
                                updated = True
        adj_set.update(new_edges)
    res = set()
    for start, label_, end in adj_set:
        if label_ == wcnf_cfg.start_symbol:
            if (not start_nodes or start in start_nodes) and (
                not final_nodes or end in final_nodes
            ):
                res.add((start, end))
    return res
