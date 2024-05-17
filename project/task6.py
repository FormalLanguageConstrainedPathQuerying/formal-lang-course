from typing import Tuple
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
import pyformlang
import networkx as nx
import queue as q
from collections import defaultdict
from .task2 import *


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    cfg.to_normal_form
    return CFG(
        start_symbol=cfg.start_symbol,
        productions=cfg._decompose_productions(
            cfg._get_productions_with_only_single_terminals()
        ),
    )


def cfpq_with_hellings(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:

    cfg = cfg_to_weak_normal_form(cfg)

    if start_nodes is None:
        start_nodes = graph.nodes

    if final_nodes is None:
        final_nodes = graph.nodes

    productions_dict = defaultdict(lambda: set())

    for v in cfg.productions:
        if len(v.body) == 0:
            continue
        productions_dict[tuple(v.body)].add(v.head)

    set_paths = set()

    _, _, edges = get_nvertex_nedges_numerate_marks_from_graph(graph)

    production_eps = {p for p in cfg.productions if len(p.body) == 0}

    # add graph terminals
    for edge in edges:
        vi, vj, label = edge
        term = Terminal(label)
        if tuple([term]) not in productions_dict:
            continue
        for i in productions_dict[tuple([term])]:
            set_paths.add((vi, i, vj))

    all_paths = {
        (vi, i.head, vi) for i in production_eps for vi in graph.nodes
    } | set_paths.copy()

    que = {i for i in all_paths}

    while len(que) > 0:

        r = que.pop()
        vi, vari, vj = r
        tmp_paths = set()

        for ui, varj, uj in all_paths:
            if ui == vj:
                if (vari, varj) in productions_dict:

                    for varNew in productions_dict[(vari, varj)]:
                        NewPath = (vi, varNew, uj)

                        if NewPath not in all_paths:
                            tmp_paths.add(NewPath)
                            que.add(NewPath)
            if uj == vi:
                if (varj, vari) in productions_dict:

                    for varNew in productions_dict[(varj, vari)]:
                        NewPath = (ui, varNew, vj)

                        if NewPath not in all_paths:
                            tmp_paths.add(NewPath)
                            que.add(NewPath)

        all_paths |= tmp_paths

    start_symbol = cfg.start_symbol

    return {
        (i, j)
        for (i, val, j) in all_paths
        if (val == start_symbol) and (i in start_nodes) and (j in final_nodes)
    }
