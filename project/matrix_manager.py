from pyformlang.finite_automaton.finite_automaton import to_state, to_symbol
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from scipy import sparse
from scipy.sparse import csr_matrix, kron

from project.boolean_matrix import BooleanMatrix


class MatrixManager:
    @staticmethod
    def from_nfa_to_boolean_matrix(automaton: NondeterministicFiniteAutomaton):
        idx_states = {state: idx for idx, state in enumerate(automaton.states)}
        start_states = automaton.start_states
        final_states = automaton.final_states

        matrix = dict()
        for source, transition in automaton.to_dict().items():
            for label, destination in transition.items():
                if not isinstance(destination, set):
                    destination = {destination}
                for state in destination:
                    idx_from = idx_states[source]
                    idx_to = idx_states[state]
                    if label not in matrix.keys():
                        number_of_states = len(automaton.states)
                        matrix[label] = sparse.csr_matrix(
                            (number_of_states, number_of_states),
                            dtype=bool,
                        )
                    matrix[label][idx_from, idx_to] = True

        return BooleanMatrix(idx_states, start_states, final_states, matrix)

    @staticmethod
    def from_boolean_matrix_to_nfa(boolean_matrix: BooleanMatrix):
        idx_states = boolean_matrix.idx_states
        start_states = boolean_matrix.start_states
        final_states = boolean_matrix.final_states
        matrix = boolean_matrix.matrix

        nfa = NondeterministicFiniteAutomaton()

        for label, matrix in matrix.items():
            [
                nfa.add_transition(
                    to_state(source), to_symbol(label), to_state(destination)
                )
                for source, destination in zip(*matrix.nonzero())
            ]

        [nfa.add_start_state(idx_states[to_state(state)]) for state in start_states]
        [nfa.add_final_state(idx_states[to_state(state)]) for state in final_states]

        return nfa

    @staticmethod
    def get_transitive_closure(boolean_matrix: BooleanMatrix) -> csr_matrix:
        if len(boolean_matrix.matrix) != 0:
            transitive_closure = sum(boolean_matrix.matrix.values())
            previous_nnz, current_nnz = transitive_closure.nnz, 0

            while previous_nnz != current_nnz:
                transitive_closure += transitive_closure @ transitive_closure
                previous_nnz, current_nnz = current_nnz, transitive_closure.nnz

            return transitive_closure
        else:
            return sparse.csr_matrix((0, 0), dtype=bool)

    @staticmethod
    def intersect_two_nfa(first: BooleanMatrix, second: BooleanMatrix) -> BooleanMatrix:
        idx_states = {}
        start_states = set()
        final_states = set()
        matrix = dict()
        labels = first.matrix.keys() & second.matrix.keys()

        for label in labels:
            matrix[label] = kron(first.matrix[label], second.matrix[label])

        for state_first, index_first in first.idx_states.items():
            for state_second, index_second in second.idx_states.items():
                new_state = index_first * len(second.idx_states) + index_second

                idx_states[new_state] = new_state

                if (
                    state_first in first.start_states
                    and state_second in second.start_states
                ):
                    start_states.add(new_state)

                if (
                    state_first in first.final_states
                    and state_second in second.final_states
                ):
                    final_states.add(new_state)

        return BooleanMatrix(idx_states, start_states, final_states, matrix)
