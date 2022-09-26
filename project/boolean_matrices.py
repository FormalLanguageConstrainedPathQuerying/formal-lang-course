from scipy import sparse
from scipy.sparse import dok_matrix
from collections import namedtuple
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

nfa_as_matrix = namedtuple(
    "nfa_as_matrix", "matrices states_count start_vector final_vector"
)


def nfa_to_boolean_matrices(
    nfa: NondeterministicFiniteAutomaton,
) -> nfa_as_matrix:
    matrix = {}
    states_count = len(nfa.states)

    if states_count == 0:
        return nfa_as_matrix(
            dok_matrix((1, 1), dtype=bool),
            0,
            dok_matrix((1, 1), dtype=bool),
            dok_matrix((1, 1), dtype=bool),
        )

    states = {old: ind for ind, old in enumerate(nfa.states)}
    for start, final_dict in nfa.to_dict().items():
        for label, final_states in final_dict.items():
            if not isinstance(final_states, set):
                final_states = {final_states}
            for final in final_states:
                if not label in matrix:
                    matrix[label] = dok_matrix((states_count, states_count), dtype=bool)
                matrix[label][states[start], states[final]] = True
    start = dok_matrix((1, states_count), dtype=bool)
    for i in nfa.start_states:
        start[0, states[i]] = True
    final = dok_matrix((1, states_count), dtype=bool)
    for i in nfa.final_states:
        final[0, states[i]] = True
    return nfa_as_matrix(matrix, states_count, start, final)


def boolean_matrices_to_nfa(matrices: nfa_as_matrix) -> NondeterministicFiniteAutomaton:
    res = NondeterministicFiniteAutomaton()
    for label in matrices.matrices:
        for start, final in zip(*matrices.matrices[label].nonzero()):
            res.add_transition(start, label, final)

    for i in matrices.start_vector.nonzero()[1]:
        res.add_start_state(i)
    for i in matrices.final_vector.nonzero()[1]:
        res.add_final_state(i)
    return res


def cross_boolean_matrices(
    first: nfa_as_matrix, second: nfa_as_matrix
) -> nfa_as_matrix:
    res = {}
    cross_labels = first.matrices.keys() & second.matrices.keys()
    for label in cross_labels:
        res[label] = sparse.kron(first.matrices[label], second.matrices[label])
    res_states_count = first.states_count * second.states_count
    res_start = sparse.kron(first.start_vector, second.start_vector)
    res_final = sparse.kron(first.final_vector, second.final_vector)
    return nfa_as_matrix(res, res_states_count, res_start, res_final)


def transitive_closure(matrix: nfa_as_matrix) -> dok_matrix:
    if len(matrix.matrices) == 0:
        return dok_matrix((matrix.states_count, matrix.states_count), dtype=bool)

    res = sum(matrix.matrices.values())
    prev_nnz = None
    curr_nnz = res.nnz
    while prev_nnz != curr_nnz:
        res += res @ res
        prev_nnz = curr_nnz
        curr_nnz = res.nnz
    return res
