from functools import reduce
from itertools import product
from networkx import MultiDiGraph
from scipy.sparse import vstack, csr_matrix

from project.task2_fa import graph_to_nfa, regex_to_dfa
from project.task3 import AdjacencyMatrixFA


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:

    dfa_adj_matrix = AdjacencyMatrixFA(regex_to_dfa(regex))
    nfa_adj_matrix = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    nfa_st_ids = {i: state for i, state in enumerate(nfa_adj_matrix.states)}

    labels = dfa_adj_matrix.adj_matrix.keys() & nfa_adj_matrix.adj_matrix.keys()

    transposed = {
        label: dfa_adj_matrix.adj_matrix[label].T for label in labels
    }

    start_states = [
        (dfa_st, nfa_st)
        for dfa_st, nfa_st in product(
            dfa_adj_matrix.start_states, nfa_adj_matrix.start_states
        )
    ]

    k = len(dfa_adj_matrix.states.keys())
    m = len(nfa_adj_matrix.states.keys())

    def init_front():
        matrices = []
        for dfa_idx, nfa_idx in start_states:
            matrix = csr_matrix((k, m), dtype=bool)
            matrix[dfa_idx, nfa_idx] = True
            matrices.append(matrix)
        return vstack(matrices, "csr", dtype=bool)

    front = init_front()
    visited = front

    # checking nnz > 0 is more efficient for sparse matrices
    while front.nnz > 0:
        new_front = []

        for label in labels:
            sym_front = front @ nfa_adj_matrix.adj_matrix[label]

            new_front.append(
                vstack(
                    [
                        transposed[label] @ sym_front[k * i : k * (i + 1)]
                        for i in range(len(start_states))
                    ]
                )
            )

        front = reduce(lambda x, y: x + y, new_front, front) > visited
        visited += front

    res = set()

    for final_dfa in dfa_adj_matrix.final_states:
        for i, start in enumerate(nfa_adj_matrix.start_states):
            reached_states = visited[k * i : k * (i + 1)].getrow(final_dfa).indices

            for reached in reached_states:
                if reached in nfa_adj_matrix.final_states:
                    res.add((nfa_st_ids[start], nfa_st_ids[reached]))

    return res
