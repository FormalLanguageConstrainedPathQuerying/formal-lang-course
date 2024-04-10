from pyformlang.cfg import CFG, Variable, Terminal
import pyformlang
import networkx as nx
from typing import *
import itertools


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

    cnf = cfg_to_weak_normal_form(cfg)
    is_epsilon = True

    triples = set()

    for edge in graph.edges(data=True):
        for production in cnf.productions:
            if (
                len(production.body) == 1
                and production.body[0].value == edge[2]["label"]
            ):
                triples.add((production.head.value, edge[0], edge[1]))
            elif len(production.body) == 0:
                is_epsilon = True

    if is_epsilon:
        for node in graph.nodes:
            triples.add(("S", node, node))

    added = True
    while added:
        added = False
        new_triples = set()
        for triple1 in triples:
            for triple2 in triples:
                if triple1[2] == triple2[1]:
                    for production in cnf.productions:
                        if (
                            len(production.body) == 2
                            and production.body[0].value == triple1[0]
                            and production.body[1].value == triple2[0]
                        ):
                            new_triple = (triple1[0], triple1[2], triple2[1])
                            if new_triple not in triples:
                                new_triples.add(new_triple)
                                added = True
                        # elif len(production.body) == 1:
                        #     if production.body[0].value == triple1[0]:
                        #         new_triple = (triple1[0], triple1[1], triple1[2])
                        #         if new_triple not in triples:
                        #             new_triples.add(new_triple)
                        #             added = True
                        #     elif production.body[0].value == triple2[0]:
                        #         new_triple = (triple2[0], triple2[1], triple2[2])
                        #         if new_triple not in triples:
                        #             new_triples.add(new_triple)
                        #             added = True

        triples.update(new_triples)

    result = set()
    for s, u, v in triples:
        if (
            s == cfg.start_symbol
            and (start_nodes is None or u in start_nodes)
            and (final_nodes is None or v in final_nodes)
        ):
            result.add((u, v))

    return result
