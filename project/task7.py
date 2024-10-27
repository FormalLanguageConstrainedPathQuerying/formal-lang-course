from pyformlang.cfg import CFG, Terminal, Production
from networkx import DiGraph
from numpy.typing import NDArray
import numpy as np
from typing import Set, Tuple
from task6 import cfg_to_weak_normal_form


def is_equal(
    old: dict[Production, NDArray[np.bool_]], new: dict[Production, NDArray[np.bool_]]
) -> bool:
    if old.keys() != new.keys():
        return False

    for prod in old.keys():
        if prod not in new.keys():
            return False

        if not np.array_equal(old, new):
            return False

    return True


def matrix_based_cfpq(
    cfg: CFG,
    graph: DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> set[tuple[int, int]]:
    wcnf = cfg_to_weak_normal_form(cfg)

    # graph = <V, E, L> | grammar = <Σ, N, P, S>

    # print(graph.edges.data('label'))
    # print(cfg.productions, cfg.terminals)

    edges_count = len(graph.edges)

    adj_matrices: dict[Production, NDArray[np.bool_]] = {}
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
                if prod not in adj_matrices.keys():
                    adj_matrices[prod] = np.zeros(shape=matrix_shape, dtype=np.bool_)

                adj_matrices[prod][i, j] = True  # 5

    for prod in wcnf.productions:
        # 𝐴 → ε
        if len(prod.body) != 0 and prod.body[0] != Epsilon:  # 6
            continue

        if prod not in adj_matrices.keys():
            adj_matrices[prod] = np.zeros(shape=matrix_shape, dtype=np.bool_)

        for i in graph.nodes:
            adj_matrices[prod][i, i] = True  # 8

    pass


from networkx import MultiDiGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon

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

matrix_based_cfpq(grammar, graph, [], [])
