from typing import Set, Dict

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import dok_matrix, kron


class BooleanMatrixAutomata:
    """
    Attributes:

    """

    number_of_states: int
    states_indexes: Dict[State, int]
    start_state_indexes: Set[int]
    final_state_indexes: Set[int]
    boolean_matrix: Dict[int, dok_matrix]

    def __init__(self, nfa: EpsilonNFA = None):
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
            self.start_state_indexes = nfa.start_states
            self.final_state_indexes = nfa.final_states
            self.boolean_matrix = self.create_boolean_matrix_from_nfa(nfa)

    def create_boolean_matrix_from_nfa(self, nfa: EpsilonNFA):
        boolean_matrix = {}
        for initial_state, labels_and_target_states in nfa.to_dict().items():
            for label, target_states in labels_and_target_states.items():
                if not isinstance(target_states, set):
                    target_states = {target_states}
                for target_state in target_states:
                    if label not in boolean_matrix:
                        boolean_matrix[label] = dok_matrix(
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
        for label, dok_matrix_self in self.boolean_matrix.items():
            matrix_array = dok_matrix_self.toarray()
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
