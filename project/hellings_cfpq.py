from typing import Any, Optional

import pyformlang.cfg as pfl_cfg
from networkx import MultiDiGraph
from pyformlang.cfg.cfg_object import CFGObject


def cfg_to_weak_normal_form(cfg: pfl_cfg.CFG) -> pfl_cfg.CFG:
    nullable = cfg.get_nullable_symbols()
    cfg = cfg.to_normal_form()
    productions = set(cfg.productions)
    for var in nullable:
        productions.add(
            pfl_cfg.Production(
                head=pfl_cfg.Variable(var.value), body=[pfl_cfg.Epsilon()]
            )
        )
    return pfl_cfg.CFG(
        start_symbol=cfg.start_symbol,
        productions=productions,
    ).remove_useless_symbols()


def hellings_based_cfpq(
    cfg: pfl_cfg.CFG,
    graph: MultiDiGraph,
    start_nodes: Optional[set[int]] = None,
    final_nodes: Optional[set[int]] = None,
) -> set[tuple[int, int]]:
    def extract_body(body: list[CFGObject]) -> list[CFGObject]:
        return [x.value for x in body]

    cfg = cfg_to_weak_normal_form(cfg)
    productions = set(cfg.productions)
    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)
    cfpq = set[tuple[Any, CFGObject, Any]]()

    label: Any
    for u, v, label in graph.edges(data="label"):
        for prod in productions:
            head, body = prod.head, prod.body
            if extract_body(body) == [label]:
                cfpq.add((u, head, v))

    for node in graph.nodes:
        for var in cfg.get_nullable_symbols():
            cfpq.add((node, var, node))

    while True:
        new_cfpq = set(
            (u1, prod.head, v2)
            for u1, x1, v1 in cfpq
            for u2, x2, v2 in cfpq
            if v1 == u2
            for prod in productions
            if prod.body == [x1, x2]
        )

        if new_cfpq.issubset(cfpq):
            break
        cfpq.update(new_cfpq)

    return {
        (u, v)
        for u, x, v in cfpq
        if v in final_nodes
        if u in start_nodes
        if x == cfg.start_symbol
    }
