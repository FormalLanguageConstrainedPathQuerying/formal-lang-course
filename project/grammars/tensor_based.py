from scipy.sparse import dok_matrix
from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from typing import Set, Tuple

from project.grammars.ecfg import ECFG
from project.utils.CFG_utils import transform_ecfg_to_rsm
from project.utils.rsm_matrix import RSMMatrix
from project.utils.automata_utils import transform_graph_to_nfa


def tensor_based(cfg: CFG, graph: MultiDiGraph) -> Set[Tuple[int, str, int]]:
    """
    Tensor Based algorithm for Context Free Path Querying

    Parameters
    ----------
    cfg: CFG
        Query given in Context Free Grammar form
    graph: MultiDiGraph
        Labeled graph for the Path Querying task

    Returns
    -------
    r: set
        Set of triplets (node, variable, node)
    """
    graph_bm = RSMMatrix.from_nfa(transform_graph_to_nfa(graph))
    rsm = transform_ecfg_to_rsm((ECFG.from_pyformlang_cfg(cfg)))
    rsm_vars = {box.variable.value for box in rsm.boxes}
    rsm_bm = RSMMatrix.from_rsm(rsm)

    for eps_state in rsm_bm.start_states & rsm_bm.final_states:
        variable = rsm_bm.get_nonterminals(eps_state, eps_state)
        if variable not in graph_bm.bmatrix:
            graph_bm.bmatrix[variable] = dok_matrix(
                (graph_bm.number_of_states, graph_bm.number_of_states), dtype=bool
            )
        for i in range(graph_bm.number_of_states):
            graph_bm.bmatrix[variable][i, i] = True

    tc = graph_bm.intersect(rsm_bm).transitive_closure()

    prev_nnz = tc.nnz
    new_nnz = 0

    while prev_nnz != new_nnz:
        for i, j in zip(*tc.nonzero()):
            rsm_from = i % rsm_bm.number_of_states
            rsm_to = j % rsm_bm.number_of_states
            variable = rsm_bm.get_nonterminals(rsm_from, rsm_to)
            if not variable:
                continue
            graph_from = i // rsm_bm.number_of_states
            graph_to = j // rsm_bm.number_of_states
            if variable not in graph_bm.bmatrix:
                graph_bm.bmatrix[variable] = dok_matrix(
                    (graph_bm.number_of_states, graph_bm.number_of_states), dtype=bool
                )
            graph_bm.bmatrix[variable][graph_from, graph_to] = True

        tc = graph_bm.intersect(rsm_bm).transitive_closure()

        prev_nnz, new_nnz = new_nnz, tc.nnz

    return {
        (u, label, v)
        for label, bm in graph_bm.bmatrix.items()
        if label in rsm_vars
        for u, v in zip(*bm.nonzero())
    }
