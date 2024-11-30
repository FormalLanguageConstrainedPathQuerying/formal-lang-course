import functools
import operator
from itertools import product

from networkx import MultiDiGraph
from scipy.sparse import csr_matrix, vstack

from project.adjacency_matrix import AdjacencyMatrixFA
from project.finite_automaton import graph_to_nfa, regex_to_dfa


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    dfa = AdjacencyMatrixFA(regex_to_dfa(regex))
    nfa = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    symbols = dfa.matrices.keys() & nfa.matrices.keys()
    permutation_matrices = {s: dfa.matrices[s].transpose() for s in symbols}

    start_states = tuple(product(dfa.start_states, nfa.start_states))

    k = dfa.states_count
    m = nfa.states_count

    def init_matrix(dfa_idx, nfa_idx):
        matrix = csr_matrix((k, m), dtype=bool)
        matrix[dfa_idx, nfa_idx] = True
        return matrix

    matrices = [init_matrix(dfa_idx, nfa_idx) for dfa_idx, nfa_idx in start_states]
    front = vstack(matrices, "csr", dtype=bool)
    visited = front

    while front.nnz > 0:
        next_front = []
        for symbol in symbols:
            symbols_front = front @ nfa.matrices[symbol]
            next_front.append(
                vstack(
                    [
                        permutation_matrices[symbol]
                        @ symbols_front[k * i : k * (i + 1)]
                        for i in range(len(start_states))
                    ]
                )
            )

        front = functools.reduce(operator.add, next_front, front) > visited
        visited = visited + front

    nfa_states = {i: state for i, state in enumerate(nfa.states)}
    res: set[tuple[int, int]] = set()
    for i, nfa_start_idx in enumerate(nfa.start_states):
        for final_dfa_state in dfa.final_states:
            reached = visited[k * i : k * (i + 1)].getrow(final_dfa_state).indices
            res.update(
                (
                    (nfa_states[nfa_start_idx], nfa_states[dfa_st_idx])
                    for dfa_st_idx in reached
                    if dfa_st_idx in nfa.final_states
                )
            )

    return res
