from typing import Set, Dict, Tuple

import networkx as nx
import numpy as np
from pyformlang.cfg import CFG, Variable, Production

from project.cfg import cfg_to_wcnf
from scipy.sparse import csr_matrix


def matrix(graph: nx.Graph, cfg: CFG) -> Set[Tuple[int, Variable, int]]:
    wcnf = cfg_to_wcnf(cfg)
    n = len(graph.nodes)
    bool_matrices = {v: csr_matrix((n, n), dtype=bool) for v in wcnf.variables}

    terminal_productions: Set[Production] = {
        p for p in wcnf.productions if len(p.body) == 1
    }
    # словарь node_number нужен, чтобы алгоритм правильно обрабатывал графы, где номера узлов начинаются не с нуля
    node_number = {node: i for (i, node) in enumerate(graph.nodes)}
    for (i, j, data) in graph.edges(data=True):
        production_heads: Set[Variable] = {
            p.head for p in terminal_productions if p.body[0].value == data["label"]
        }
        for v in production_heads:
            bool_matrices[v][node_number[i], node_number[j]] = True

    # добавляем петли за счет эпсилон продукций
    epsilon_productions_heads = {p.head for p in wcnf.productions if not p.body}
    for v in epsilon_productions_heads:
        for i in range(n):
            bool_matrices[v][i, i] = True

    variables_productions = {p for p in wcnf.productions if len(p.body) == 2}
    is_changed = True
    while is_changed:
        is_changed = False
        # A_i -> A_j A_k
        for p in variables_productions:
            old_nnz = bool_matrices[p.head].nnz
            bool_matrices[p.head] += bool_matrices[p.body[0]] @ bool_matrices[p.body[1]]
            is_changed |= old_nnz != bool_matrices[p.head].nnz

    # redefine node_number dict
    node_number = {number: node for (node, number) in node_number.items()}

    return {
        (node_number[i], v, node_number[j])
        for v, mat in bool_matrices.items()
        for (i, j) in zip(*mat.nonzero())
    }
