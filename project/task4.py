import scipy.sparse as sp
from project.task2 import regex_to_dfa, graph_to_nfa
from networkx import MultiDiGraph
from project.task3 import AdjacencyMatrixFA
from functools import reduce
from collections import defaultdict


def init_front(
    start_states_r: set[int], start_states_g: set[int], regex_size, graph_size
) -> sp.csr_matrix:
    matrices = []
    for g_start in start_states_g:
        M = sp.lil_matrix((regex_size, graph_size))
        for r_start in start_states_r:
            M[r_start, g_start] = 1
        matrices.append(M)

    final_M = sp.vstack(matrices, format="csr")

    return final_M


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_adj = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_adj = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    if len(graph_adj.start_state_indices) == 0:
        return set()

    regex_size = regex_adj.total_states
    graph_size = graph_adj.total_states

    reachable = set()
    symbols = set(regex_adj.transition_matrices).intersection(
        graph_adj.transition_matrices
    )

    front = init_front(
        regex_adj.start_state_indices,
        graph_adj.start_state_indices,
        regex_size,
        graph_size,
    )
    visited = front

    while True:
        fronts = defaultdict(lambda: sp.csr_matrix(front.shape, dtype=bool))
        for symbol in symbols:
            new_front = front @ graph_adj.transition_matrices[symbol]
            for start in range(len(graph_adj.start_state_indices)):
                batch = start * regex_size
                rows, cols = regex_adj.transition_matrices[symbol].nonzero()
                row_indices = [batch + row for row in rows]
                col_indices = [batch + col for col in cols]
                fronts[symbol][col_indices, :] += new_front[row_indices, :]

        front = reduce(
            lambda x, y: x + y, fronts.values(), sp.csr_matrix(front.shape, dtype=bool)
        )
        front = front > visited
        if (front > visited).nnz == 0:
            break
        visited += front

    for fn_reg in regex_adj.final_state_indices:
        for st_idx, st in enumerate(graph_adj.start_state_indices):
            visited_slice = visited[regex_size * st_idx : regex_size * (st_idx + 1)]
            row = visited_slice.getrow(fn_reg).toarray()[0]
            non_zero_indices = row.nonzero()[0]
            for reached in non_zero_indices:
                if reached in graph_adj.final_state_indices:
                    reachable.add(
                        (
                            graph_adj.index_state[st],
                            graph_adj.index_state[reached],
                        )
                    )

    return reachable
