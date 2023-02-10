from typing import Set, Tuple, Union

import networkx as nx
from pyformlang.cfg import CFG, Variable
from project.cfg import cfg_to_wcnf


def hellings(graph: nx.Graph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    wcnf = cfg_to_wcnf(cfg)

    r = {
        (N, v, v)
        for v in graph.nodes
        for N in {p.head.value for p in wcnf.productions if not p.body}
    }.union(
        {
            (N, v, u)
            for (v, u, data) in graph.edges(data=True)
            for N in {
                p.head.value
                for p in wcnf.productions
                if p.body[0].value == data["label"]
            }
        }
    )
    m = r.copy()

    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    while m != set():
        # N_i -> v--u
        N_i, v, u = m.pop()
        new_triplets = set()

        # пробуем пристроить путь слева к v--u
        # N_j -> v1--v2
        # новый путь v1--v2==v--u (в итоге v1--u)
        for (N_j, v1, v2) in r:
            if v2 == v:
                for N_k in {
                    p.head.value for p in var_productions if p.body == [N_j, N_i]
                }:
                    if (N_k, v1, u) not in r:
                        new_triplets.add((N_k, v1, u))
        m.update(new_triplets)
        r.update(new_triplets)
        new_triplets.clear()

        # пробуем пристроить путь справа к v--u
        # N_j -> v1--v2
        # новый путь v--u==v1--v2 (в итоге v--v2)
        for (N_j, v1, v2) in r:
            if v1 == u:
                for N_k in {
                    p.head.value for p in var_productions if p.body == [N_i, N_j]
                }:
                    if (N_k, v, v2) not in r:
                        new_triplets.add((N_k, v, v2))
        m.update(new_triplets)
        r.update(new_triplets)
        new_triplets.clear()

    # переупорядочиваем, чтобы соответствовать требованию в домашке
    return {(v1, N, v2) for (N, v1, v2) in r}
