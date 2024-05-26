import copy
from typing import Set, Tuple
import pyformlang
from pyformlang.cfg import Terminal, Epsilon
from pyformlang.cfg.cfg import CFG, Variable
import networkx as nx


def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
    grammatical = (cfg.
                   eliminate_unit_productions().
                   remove_useless_symbols())
    _new_productions = (grammatical.
    _decompose_productions(
        grammatical._get_productions_with_only_single_terminals()
    ))
    return CFG(start_symbol=grammatical.start_symbol,
               productions=_new_productions)


def cfg_from_file(path: str) -> CFG:
    with open(path) as f:
        return CFG.from_text(f.read())


def cfpq_with_hellings(
        cfg: pyformlang.cfg.CFG,
        graph: nx.DiGraph,
        start_nodes: Set[int] = None,
        final_nodes: Set[int] = None,
) -> Set[Tuple[int, int]]:
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    grammatics = cfg_to_weak_normal_form(cfg)
    p_1 = {}
    p_2 = set()
    p_3 = {}

    for _production in grammatics.productions:
        if (len(_production.body) == 1 and
                isinstance(_production.body[0], Terminal)):
            p_1.setdefault(
                _production.head, set()
            ).add(_production.body[0])
        elif (len(_production.body) == 1 and
              isinstance(_production.body[0], Epsilon)):
            p_2.add(_production.body[0])
        elif len(_production.body) == 2:
            (p_3.setdefault(
                _production.head,
                set()
            )
             .add((_production.body[0], _production.body[1]))
             )

    result = {(n_i, vertice, vertice) for n_i in p_2 for vertice in graph.nodes}
    result |= {
        (n_i, v_i, u_i)
        for (v_i, u_i, tag) in graph.edges.data("label")
        for n_i in p_1
        if tag in p_1[n_i]
    }

    queue = copy.deepcopy(result)

    while len(queue) > 0:
        n_i, v_i, u_i = queue.pop()

        step_increment = set()
        for N_j, v_, u_ in result:
            if v_i == u_:
                for N_k in p_3:
                    if (N_j, n_i) in p_3[N_k] and (N_k, v_, v_i) not in result:
                        queue.add((N_k, v_, u_i))
                        step_increment.add((N_k, v_, u_i))
        result |= step_increment

    answer = {
        (v_i, u_i)
        for (n_i, v_i, u_i) in result
        if v_i in start_nodes and u_i in final_nodes and Variable(n_i) == cfg.start_symbol
    }

    return answer


if __name__ == '__main__':
    pass
