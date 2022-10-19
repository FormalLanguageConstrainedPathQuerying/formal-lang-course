from typing import Set, Dict

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import dok_matrix, kron, block_diag, vstack


class BooleanMatrixAutomata:
    number_of_states: int
    states_indexes: Dict[State, int]
    start_state_indexes: Set[int]
    final_state_indexes: Set[int]
    type_of_matrix = dok_matrix
    boolean_matrix: Dict[int, type_of_matrix]

    def __init__(self, nfa: EpsilonNFA = None, tom=dok_matrix):
        if nfa is None:
            self.number_of_states = 0
            self.states_indexes = dict()
            self.start_state_indexes = set()
            self.final_state_indexes = set()
            self.boolean_matrix = dict()
        else:
            self.number_of_states = len(nfa.states)
            self.states_indexes = {
                state: index for (index, state) in enumerate(nfa.states)
            }
            self.start_state_indexes = {i.value for i in nfa.start_states}
            self.final_state_indexes = {i.value for i in nfa.final_states}
            self.boolean_matrix = self.create_boolean_matrix_from_nfa(nfa)
        self.type_of_matrix = tom

    def create_boolean_matrix_from_nfa(self, nfa: EpsilonNFA):
        boolean_matrix = {}
        for initial_state, labels_and_target_states in nfa.to_dict().items():
            for label, target_states in labels_and_target_states.items():
                if not isinstance(target_states, set):
                    target_states = {target_states}
                for target_state in target_states:
                    if label not in boolean_matrix:
                        boolean_matrix[label] = self.type_of_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool
                        )
                    boolean_matrix[label][
                        self.states_indexes[initial_state],
                        self.states_indexes[target_state],
                    ] = True
        return boolean_matrix

    def create_nfa_from_boolean_matrix(self):
        nfa = EpsilonNFA()
        for state in self.start_state_indexes:
            nfa.add_start_state(State(state))
        for state in self.final_state_indexes:
            nfa.add_final_state(State(state))
        for label, matrix_self in self.boolean_matrix.items():
            matrix_array = matrix_self.toarray()
            for initial_state, i in self.states_indexes.items():
                for target_state, j in self.states_indexes.items():
                    if matrix_array[i][j]:
                        nfa.add_transition(initial_state, label, target_state)
        return nfa

    def intersect(self, second: "BooleanMatrixAutomata"):
        bma = BooleanMatrixAutomata()
        bma.number_of_states = self.number_of_states * second.number_of_states

        bma.boolean_matrix = {
            label: kron(self.boolean_matrix[label], second.boolean_matrix[label])
            for label in (self.boolean_matrix.keys() & second.boolean_matrix.keys())
        }

        for (first_state, first_index) in self.states_indexes.items():
            for (second_state, second_index) in second.states_indexes.items():
                state_index = first_index * second.number_of_states + second_index
                bma.states_indexes[State(state_index)] = state_index
                if (
                    first_state in self.start_state_indexes
                    and second_state in second.start_state_indexes
                ):
                    bma.start_state_indexes.add(state_index)
                if (
                    first_state in self.final_state_indexes
                    and second_state in second.final_state_indexes
                ):
                    bma.final_state_indexes.add(state_index)
        return bma

    def transitive_closure(self):
        trans_closure = sum(self.boolean_matrix.values())
        prev_value = trans_closure.nnz
        curr_value = 0

        while prev_value != curr_value:
            trans_closure += trans_closure @ trans_closure
            prev_value = curr_value
            curr_value = trans_closure.nnz
        return trans_closure

    def bfs_based_rpq(self, second: "BooleanMatrixAutomata", separately: bool):
        self_n = self.number_of_states
        second_n = second.number_of_states

        def get_front(start_states=None):
            front1 = self.type_of_matrix((second_n, self_n + second_n), dtype=bool)

            front_for_self = self.type_of_matrix((1, self_n), dtype=bool)
            for i in start_states:
                front_for_self[0, i] = True
            for ss in second.start_state_indexes:
                i = second.states_indexes[State(ss)]
                front1[i, i] = True
                front1[[i], second_n:] = front_for_self
            return front1

        def transform_rows(front_part):
            new_fp = self.type_of_matrix(front_part.shape, dtype=bool)
            xx, yy = front_part.nonzero()
            for ii, jj in zip(xx, yy):
                if jj < second_n:
                    row_second_part = front_part[[ii], second_n:]
                    if row_second_part.nnz > 0:
                        shift = ii - ii % second_n
                        new_fp[shift + jj, jj] = True
                        new_fp[[shift + jj], second_n:] += row_second_part
            return new_fp

        direct_sum = {
            label: block_diag(
                (second.boolean_matrix[label], self.boolean_matrix[label])
            )
            for label in (self.boolean_matrix.keys() & second.boolean_matrix.keys())
        }

        front = (
            vstack([get_front({i}) for i in self.start_state_indexes])
            if separately
            else get_front(self.start_state_indexes)
        )

        visited = self.type_of_matrix(front.shape, dtype=bool)
        is_first_step = True
        while True:
            visited_nnz = visited.nnz
            for _, matrix in direct_sum.items():
                new_front_part = front @ matrix if is_first_step else visited @ matrix
                visited += transform_rows(new_front_part)
            is_first_step = False
            if visited_nnz == visited.nnz:
                break

        answer = set()
        second_states = list(second.states_indexes.keys())
        self_states = list(self.states_indexes.keys())
        x, y = visited.nonzero()
        for i, j in zip(x, y):
            if (
                j >= second_n
                and second_states[i % second_n] in second.final_state_indexes
            ):
                state_index = j - second_n
                if self_states[state_index] in self.final_state_indexes:
                    if separately:
                        answer.add((State(i // second_n), State(state_index)))
                    else:
                        answer.add(State(state_index))
        copy = answer
        if separately:
            answer = {}
            for i in copy:
                answer.setdefault(i[0], []).append(i[1])
        return answer
