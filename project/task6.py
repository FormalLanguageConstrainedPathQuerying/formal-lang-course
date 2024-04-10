from pyformlang.cfg import CFG, Variable, Terminal
import pyformlang
import networkx as nx
from typing import *


def read_cfgrammar(path, start="S") -> CFG:
    with open(path, "r") as f:
        text = f.read()
        return CFG.from_text(text, Variable(start))


def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
    elimUnit = cfg.eliminate_unit_productions()
    elimUnitUseless = elimUnit.remove_useless_symbols()
    productions = elimUnitUseless._decompose_productions(
        elimUnitUseless._get_productions_with_only_single_terminals()
    )
    return CFG(productions=set(productions), start_symbol=Variable("S"))


def cfpq_with_hellings(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    cfg = cfg_to_weak_normal_form(cfg)

    R = set()

    terminals_to_variables = {}
    for rule in cfg.productions:
        if len(rule.body) == 1 and isinstance(rule.body[0], pyformlang.cfg.Terminal):
            terminal = rule.body[0]
            if terminal not in terminals_to_variables:
                terminals_to_variables[terminal] = set()
            terminals_to_variables[terminal].add(rule.head)

    for edge in graph.edges(data=True):
        u, v, data = edge
        if data["label"] in terminals_to_variables:
            for variable in terminals_to_variables[data["label"]]:
                R.add((u, variable, v))

    changed = True
    while changed:
        changed = False
        new_R = set()
        for u, A, v in R:
            for s, B, t in R:
                if t == u:
                    for rule in cfg.productions:
                        if rule.body == [B, A]:
                            if (s, rule.head, v) not in R:
                                new_R.add((s, rule.head, v))
                                changed = True
                if s == v:
                    for rule in cfg.productions:
                        if rule.body == [A, B]:
                            if (u, rule.head, t) not in R:
                                new_R.add((u, rule.head, t))
                                changed = True
        R |= new_R

    result = {(u, v) for u, A, v in R if A == cfg.start_symbol}

    if start_nodes:
        result = {pair for pair in result if pair[0] in start_nodes}
    if final_nodes:
        result = {pair for pair in result if pair[1] in final_nodes}

    return result
