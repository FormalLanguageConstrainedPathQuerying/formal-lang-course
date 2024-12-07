from typing import Any, Optional

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from pyformlang.cfg.cfg_object import CFGObject
from scipy.sparse import csr_matrix

from project.hellings_cfpq import cfg_to_weak_normal_form


def extract_body(body: list[CFGObject]) -> list[CFGObject]:
    return [x.value for x in body]


def matrix_based_cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_nodes: Optional[set[int]] = None,
    final_nodes: Optional[set[int]] = None,
) -> set[tuple[int, int]]:
    cfg = cfg_to_weak_normal_form(cfg)
    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)

    nodes, n = graph.nodes, len(graph)
    node_to_i = {node: i for i, node in enumerate(nodes)}
    i_to_node = {i: node for i, node in enumerate(nodes)}

    decomposition: dict[CFGObject, csr_matrix] = {
        variable: csr_matrix((n, n), dtype=bool) for variable in cfg.variables
    }

    label: Any
    for u, v, label in graph.edges.data("label"):
        for prod in cfg.productions:
            head, body = prod.head, prod.body
            if extract_body(body) == [label]:
                decomposition[head][node_to_i[u], node_to_i[v]] = True

    for var in cfg.get_nullable_symbols():
        decomposition[var].setdiag(True)

    q = set(cfg.variables)
    while q:
        var = q.pop()
        for prod in cfg.productions:
            head, body = prod.head, prod.body
            if len(body) == 2:
                var1, var2 = body
                if var1 != var and var2 != var:
                    continue
                head_matrix = decomposition[head] + (
                    decomposition[var1] @ decomposition[var2]
                )
                if (decomposition[head] != head_matrix).nnz:
                    decomposition[head] = head_matrix
                    q.add(head)

    return set(
        (i_to_node[u], i_to_node[v])
        for u, v in zip(*decomposition[cfg.start_symbol].nonzero())
        if i_to_node[u] in start_nodes
        if i_to_node[v] in final_nodes
    )
