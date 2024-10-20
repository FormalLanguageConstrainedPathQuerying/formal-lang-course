from typing import Set, Tuple
import networkx as nx
from pyformlang.cfg import CFG, Production, Terminal, Epsilon, Variable


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    new_productions = set(cfg.to_normal_form().productions) | {
        Production(Variable(var.value), [Epsilon()])
        for var in cfg.get_nullable_symbols()
    }

    return CFG(
        start_symbol=cfg.start_symbol, productions=new_productions
    ).remove_useless_symbols()


def hellings_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    weak_nf_grammar = cfg_to_weak_normal_form(cfg)

    term_vars_map = {}
    vars_body_map = {}

    for prod in weak_nf_grammar.productions:
        if len(prod.body) == 1 and isinstance(prod.body[0], Terminal):
            term_vars_map.setdefault(prod.body[0], set()).add(prod.head)
        elif len(prod.body) == 2:
            vars_body_map.setdefault(tuple(prod.body), set()).add(prod.head)

    new_edges = set()
    for src, tgt, label in graph.edges.data("label"):
        term = Terminal(label)
        if term in term_vars_map:
            for var in term_vars_map[term]:
                new_edges.add((src, var, tgt))

    for node in graph.nodes:
        for var in weak_nf_grammar.get_nullable_symbols():
            new_edges.add((node, var, node))

    def process_edges(s1, a, f1, s2, b, f2):
        return (
            [
                (s1, head_var, f2)
                for head_var in vars_body_map[(a, b)]
                if (s1, head_var, f2) not in new_edges
            ]
            if f1 == s2 and (a, b) in vars_body_map
            else []
        )

    q = list(new_edges)
    while q:
        edge1 = q.pop(0)
        buffer = set()
        for edge2 in new_edges:
            edges = [*process_edges(*edge1, *edge2), *process_edges(*edge2, *edge1)]
            buffer |= set(edges)
            for edge in edges:
                q.append(edge)
        new_edges |= buffer

    return {
        (src, tgt)
        for src, var, tgt in new_edges
        if src in start_nodes
        and var == weak_nf_grammar.start_symbol
        and tgt in final_nodes
    }
