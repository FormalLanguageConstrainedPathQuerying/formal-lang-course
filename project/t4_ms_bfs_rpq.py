from project import t2_fa_utils as t2
from project import t3_graph_fa as t3
from networkx import MultiDiGraph
import scipy.sparse as sp


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    reg_dfa = t2.regex_to_dfa(regex)
    graph_nfa = t2.graph_to_nfa(graph, start_nodes, final_nodes)

    reg_am = t3.AdjacencyMatrixFA(reg_dfa)
    graph_am = t3.AdjacencyMatrixFA(graph_nfa)

    dfa_m = reg_am.n_states
    nfa_n = graph_am.n_states

    new_alphabet = reg_am.alphabet & graph_am.alphabet

    start_states = []
    for dfa_state in reg_dfa.start_states:
        for nfa_state in graph_nfa.start_states:
            start_states.append((dfa_state, nfa_state))

    # create initial frontier matrices for each start state
    matrices = []
    for dfa_state, nfa_state in start_states:
        matrix = sp.csc_matrix((dfa_m, nfa_n), dtype=bool)
        dfa_idx = list(reg_dfa.states).index(dfa_state)
        nfa_idx = list(graph_nfa.states).index(nfa_state)
        matrix[dfa_idx, nfa_idx] = True
        matrices.append(matrix)

    front = sp.vstack(matrices, format="csc", dtype=bool)
    visited = front.copy()

    # create permutation matrices for dfa transitions
    permutation_matrices = {}
    for symbol in new_alphabet:
        if symbol in reg_am.transitions:
            permutation_matrices[symbol] = reg_am.transitions[symbol].transpose()

    while front.nnz > 0:
        symbol_fronts = []

        for symbol in new_alphabet:
            if symbol in graph_am.transitions and symbol in permutation_matrices:
                symbol_front = front @ graph_am.transitions[symbol]

                # apply dfa permutation for each start state
                permuted_fronts = []
                for idx in range(len(start_states)):
                    start_slice = symbol_front[dfa_m * idx : dfa_m * (idx + 1)]
                    permuted = permutation_matrices[symbol] @ start_slice
                    permuted_fronts.append(permuted)

                symbol_fronts.append(sp.vstack(permuted_fronts, format="csc"))

        if symbol_fronts:
            # combine all symbol frontiers by adding them
            new_front = symbol_fronts[0]
            for i in range(1, len(symbol_fronts)):
                new_front = new_front + symbol_fronts[i]
            new_front.data[:] = True

            # remove already visited states
            front = new_front.multiply(visited == 0)
            visited = visited + front
        else:
            break

    result = set()
    for idx, (dfa_start_state, nfa_start_state) in enumerate(start_states):
        states_slice = visited[dfa_m * idx : dfa_m * (idx + 1)]
        rows, cols = states_slice.nonzero()

        for dfa_idx, nfa_idx in zip(rows, cols):
            dfa_state = list(reg_dfa.states)[dfa_idx]
            nfa_state = list(graph_nfa.states)[nfa_idx]

            # check if both states are final
            if (
                dfa_state in reg_dfa.final_states
                and nfa_state in graph_nfa.final_states
            ):
                result.add((nfa_start_state.value, nfa_state.value))

    return result
