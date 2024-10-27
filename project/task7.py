from pyformlang.cfg import CFG, Terminal, Production
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

    # print(graph.edges.data('label'))
    # print(cfg.productions, cfg.terminals)

    adj_matrices: dict[str, NDArray[np.bool_]] = {}
    matrix_shape = (len(graph.edges), len(graph.edges))
    inf_rules: list[Production] = []

    terminal_values = [t.value for t in cfg.terminals]

    # fill adj matrices
    for n, m, label in graph.edges.data("label"):
        if label is None:
            continue

        # a ∈ Σ ∩ L
        if label not in terminal_values:
            continue

        have_prod = False

        # 𝐴 → ε
        if n == m:  # (i, i)
            for prod in wcnf.productions:
                if len(prod.body) == 0 or prod.body[0] == Epsilon:
                    inf_rules.append(prod)
                    have_prod = True

        # A → a
        for prod in wcnf.productions:
            if len(prod.body) > 0 and prod.body[0].value == label:
                inf_rules.append(prod)
                have_prod = True

        if not have_prod:
            continue

        if label not in adj_matrices.keys():
            adj_matrices[label] = np.zeros(shape=matrix_shape, dtype=np.bool_)

        adj_matrices[label][n, m] = True

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
