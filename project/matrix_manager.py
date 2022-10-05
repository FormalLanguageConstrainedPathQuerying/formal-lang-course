from pyformlang.finite_automaton.finite_automaton import (
    to_state,
    to_symbol,
    FiniteAutomaton,
)
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse
from scipy.sparse import csr_matrix, kron, lil_array, vstack, lil_matrix

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

    @staticmethod
    def _calc_direct_sum(first: BooleanMatrix, second: BooleanMatrix) -> BooleanMatrix:
        first_states_len = len(first.idx_states)
        second_states_len = len(second.idx_states)

        idx_states = dict()
        for _, first_index in first.idx_states.items():
            for _, second_index in second.idx_states.items():
                state = first_index * second_states_len + second_index
                idx_states[state] = state

        start_states = first.start_states | {
            State(state.value + first_states_len) for state in second.start_states
        }
        final_states = first.final_states | {
            State(state.value + first_states_len) for state in second.final_states
        }

        symbols = first.matrix.keys() & second.matrix.keys()
        matrix = dict()
        for symbol in symbols:
            matrix[symbol] = sparse.bmat(
                [
                    [first.matrix[symbol], None],
                    [None, second.matrix[symbol]],
                ]
            )

        return BooleanMatrix(idx_states, start_states, final_states, matrix)

    @staticmethod
    def _transform_front(front: csr_matrix, states_num: int) -> csr_matrix:
        transformed_front = lil_array(front.shape)

        for (i, j) in zip(*front.nonzero()):
            if j < states_num:
                non_zero_row_right = front.getrow(i).tolil()[[0], states_num:]

                if non_zero_row_right.nnz > 0:
                    row_shift = i // states_num * states_num
                    transformed_front[row_shift + j, j] = 1
                    transformed_front[
                        [row_shift + j], states_num:
                    ] += non_zero_row_right

        return transformed_front.tocsr()

    @staticmethod
    def _construct_single_front(
        first: BooleanMatrix, second: BooleanMatrix
    ) -> csr_matrix:
        first_states_len = len(first.idx_states)
        second_states_len = len(second.idx_states)

        first_states = MatrixManager.from_boolean_matrix_to_nfa(first).states
        front = lil_matrix((second_states_len, second_states_len + first_states_len))

        right_part_front = lil_array(
            [[state in first.start_states for state in first_states]]
        )

        for _, idx in second.idx_states.items():
            front[idx, idx] = True
            front[idx, second_states_len:] = right_part_front

        return front.tocsr()

    @staticmethod
    def _construct_front(
        first: BooleanMatrix, second: BooleanMatrix, separate: bool
    ) -> csr_matrix:
        first_states_len = len(first.idx_states)
        second_states_len = len(second.idx_states)

        if separate:
            start_state_idx = {
                idx
                for idx in range(first_states_len)
                if first.idx_states[idx] in first.start_states
            }

            fronts = [
                MatrixManager._construct_single_front(first, second)
                for _ in start_state_idx
            ]

            if len(fronts) > 0:
                return csr_matrix(vstack(fronts))
            else:
                return csr_matrix(
                    (second_states_len, second_states_len + first_states_len)
                )
        else:
            return MatrixManager._construct_single_front(first, second)

    @staticmethod
    def bfs(first: FiniteAutomaton, second: FiniteAutomaton, separate: bool) -> set:
        first_states = first.states
        second_states = second.states

        first = MatrixManager.from_nfa_to_boolean_matrix(first)
        second = MatrixManager.from_nfa_to_boolean_matrix(second)

        direct_sum = MatrixManager._calc_direct_sum(second, first)
        first_states_len = len(first.idx_states)
        second_states_len = len(second.idx_states)

        first_start_state_idx = [
            idx for idx, state in enumerate(first_states) if state in first.start_states
        ]

        first_final_state_idx = [
            idx for idx, state in enumerate(first_states) if state in first.final_states
        ]

        second_final_state_indices = [
            idx
            for idx, state in enumerate(second_states)
            if state in second.final_states
        ]

        front = MatrixManager._construct_front(first, second, separate)
        visited = csr_matrix(front.shape)

        while True:
            visited_copy = visited.copy()

            for _, matrix in direct_sum.matrix.items():
                alt_front = visited @ matrix if front is None else front @ matrix
                visited += MatrixManager._transform_front(alt_front, second_states_len)
            front = None

            if visited.nnz == visited_copy.nnz:
                break

        result = set()
        for (i, j) in zip(*visited.nonzero()):
            if (
                j >= second_states_len
                and i % second_states_len in second_final_state_indices
            ):
                if j - second_states_len in first_final_state_idx:
                    result.add(
                        j - second_states_len
                        if not separate
                        else (
                            first_start_state_idx[i // first_states_len],
                            j - second_states_len,
                        )
                    )

        return result
