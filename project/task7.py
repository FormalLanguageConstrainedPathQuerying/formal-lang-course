from pyformlang.cfg import CFG
import networkx as nx
from typing import Set
from project.task6 import cfg_to_weak_normal_form
from scipy.sparse import csr_matrix

def matrix_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:

    weak_normal_form = cfg_to_weak_normal_form(cfg)
    node_to_idx = {node: index for index, node in enumerate(graph.nodes)}
    idx_to_node = {index: node for node, index in node_to_idx.items()}

    eps_prods = list()
    term_prods = list()
    var_prods = list()
    for production in weak_normal_form.productions:
        if not production.body:
            eps_prods.append(production.head.value)
        elif len(production.body) == 1:
            term_prods.append(production)
        elif len(production.body) == 2:
            var_prods.append(production)

    bool_decomposition = dict()
    for var in weak_normal_form.variables:
        bool_decomposition[var] = csr_matrix(
            (graph.number_of_nodes(), graph.number_of_nodes()), dtype=bool
        )

    for eps in eps_prods:
        bool_decomposition[eps].setdiag(True)

    for i, j, data in graph.edges(data=True):
        label = data["label"]
        for production in term_prods:
            if production.body[0].value == label:
                bool_decomposition[production.head][node_to_idx[i], node_to_idx[j]] = True

    changed = True
    while changed:
        changed = False
        for production in var_prods:
            old = bool_decomposition[production.head.value].nnz
            new_matrix = bool_decomposition[production.body[0].value] @ bool_decomposition[production.body[1].value]
            bool_decomposition[production.head.value] += new_matrix
            new = bool_decomposition[production.head.value].nnz
            changed = changed or (old != new)

    result = set()
    start_var = weak_normal_form.start_symbol
    if start_var not in bool_decomposition:
        return result

    for start, final in zip(*bool_decomposition[start_var].nonzero()):
        if idx_to_node[start] in start_nodes and idx_to_node[final] in final_nodes:
            result.add((idx_to_node[start], idx_to_node[final]))

    return result
