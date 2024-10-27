from pyformlang.cfg import CFG, Terminal, Production, Variable, Epsilon
from networkx import DiGraph
from numpy.typing import NDArray
import numpy as np
from typing import Set, Tuple
from project.task6 import cfg_to_weak_normal_form


def matrix_based_cfpq(
    cfg: CFG,
    graph: DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    wcnf = cfg_to_weak_normal_form(cfg)

    # graph = <V, E, L> | grammar = <Σ, N, P, S>

    edges_count = len(graph.edges)

    adj_matrices: dict[Variable, NDArray] = {}
    matrix_shape = (edges_count, edges_count)

    terminal_values = [t.value for t in cfg.terminals]

    # fill adj matrices
    for i, j, label in graph.edges.data("label"):
        # a ∈ Σ ∩ L
        if label is None or label not in terminal_values:
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

        for i in graph.nodes:
            adj_matrices[A][i, i] = True  # 8

    while True:
        changed = False

        for prod in wcnf.productions:
            if len(prod.body) == 2:
                A = prod.head
                B = prod.body[0]
                C = prod.body[1]

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

    for i in start:
        for j in final:
            if T[i, j]:
                pairs.add((i, j))

    return pairs


from networkx import MultiDiGraph

graph = MultiDiGraph()
graph.add_edges_from(
    [(0, 1, dict(label="b")), (1, 2, dict(label="b")), (2, 0, dict(label="b"))]
)

var_S = Variable("S")
var_B = Variable("B")

ter_a = Terminal("a")
ter_b = Terminal("b")
ter_c = Terminal("c")

# Creation of productions
p0 = Production(var_S, [var_S, ter_b])
p1 = Production(var_S, [])

grammar = CFG({var_S}, {ter_b}, var_S, {p0, p1})

print(matrix_based_cfpq(grammar, graph))
