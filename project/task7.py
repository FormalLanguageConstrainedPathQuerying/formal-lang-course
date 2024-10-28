from pyformlang.cfg import CFG, Terminal, Production, Variable, Epsilon
from networkx import DiGraph
from numpy.typing import NDArray
import numpy as np
from typing import Set, Tuple
from task6 import cfg_to_weak_normal_form


def matrix_based_cfpq(
    cfg: CFG,
    graph: DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    wcnf = cfg_to_weak_normal_form(cfg)

    # graph = <V, E, L> | grammar = <Σ, N, P, S>

    nodes_count = len(graph.nodes)

    adj_matrices: dict[Variable, NDArray] = {}
    matrix_shape = (nodes_count, nodes_count)

    terminal_values = [t.value for t in cfg.terminals]

    # fill adj matrices
    for n, m, label in graph.edges.data("label"):
        i = list(graph.nodes).index(n)
        j = list(graph.nodes).index(m)

        # a ∈ Σ ∩ L
        if (label is None) or (label not in terminal_values):
            continue

        # A → a
        for prod in wcnf.productions:
            if len(prod.body) > 0 and prod.body[0].value == label:
                A = prod.head
                if A not in adj_matrices.keys():
                    adj_matrices[A] = np.zeros(shape=matrix_shape, dtype=np.bool_)

                adj_matrices[A][i, j] = True  # 5

    for prod in wcnf.productions:
        A = prod.head
        # 𝐴 → ε
        if len(prod.body) != 0 and prod.body[0] != Epsilon:  # 6
            continue

        if A not in adj_matrices.keys():
            adj_matrices[A] = np.zeros(shape=matrix_shape, dtype=np.bool_)

        for i, _ in enumerate(graph.nodes):
            adj_matrices[A][i, i] = True  # 8

    print(adj_matrices)

    # is empty
    if len(adj_matrices.keys()) == 0:
        return set()

    while True:
        vars = adj_matrices.keys()
        changed = False

        for prod in wcnf.productions:
            if len(prod.body) == 2:
                A = prod.head
                B = prod.body[0]
                C = prod.body[1]

                if A not in vars or B not in vars or C not in vars:
                    continue

                mult = adj_matrices[B] @ adj_matrices[C]
                res = adj_matrices[A] + mult

                if not (res == adj_matrices[A]).all():
                    changed = True
                    adj_matrices[A] = res

        if not changed:
            break

    start = graph.nodes if start_nodes is None else start_nodes
    final = graph.nodes if final_nodes is None else final_nodes

    T = adj_matrices[wcnf.start_symbol]
    pairs: set[tuple[int, int]] = set()

    for i, node_i in enumerate(graph.nodes):
        for j, node_j in enumerate(graph.nodes):
            if node_i in start and node_j in final and T[i, j]:
                pairs.add((node_i, node_j))

    return pairs


from networkx import MultiDiGraph

# {S -> S Terminal(a), S -> }
# []
# [1] [1]

graph = MultiDiGraph()
graph.add_edges_from([(0, 1, dict(label = "b")), (1, 2, dict(label = "b")), (2, 0, dict(label = "b"))])
# graph.add_edges_from([(0, 1, dict(label="b"))])

grammar = CFG.from_text("S -> S b b | $")

print(matrix_based_cfpq(grammar, graph))
