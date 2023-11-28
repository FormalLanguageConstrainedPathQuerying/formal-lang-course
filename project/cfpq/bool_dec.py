from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy.sparse import dok_matrix, kron


class BooleanDecomposition:
    def __init__(self, automaton: NondeterministicFiniteAutomaton = None):
        if automaton is None:
            self.num_states = 0
            self.start_states = set()
            self.final_states = set()
            self.bool_matrices = {}
            self.state_indexes = {}
        else:
            self.num_states = len(automaton.states)
            self.state_indexes = {
                state: index for index, state in enumerate(automaton.states)
            }
            self.start_states = automaton.start_states
            self.final_states = automaton.final_states
            self.bool_matrices = self._create_boolean_matrices(automaton)
        self.states_to_box_variable = {}

    def transitive_closure(self):
        if not self.bool_matrices.values():
            return dok_matrix((1, 1))
        tc = sum(bm for bm in self.bool_matrices.values())
        prev_nnz = tc.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc += tc @ tc
            prev_nnz, new_nnz = new_nnz, tc.nnz

        return tc

    @classmethod
    def from_automaton(cls, automaton):
        decomposition = cls()
        decomposition.num_states = len(automaton.states)
        decomposition.start_states = automaton.start_states
        decomposition.final_states = automaton.final_states
        decomposition.state_indexes = {
            state: idx for idx, state in enumerate(automaton.states)
        }
        decomposition.bool_matrices = decomposition._create_boolean_matrices(automaton)
        return decomposition

    def intersect(self, other):
        result = BooleanDecomposition()
        result.num_states = self.num_states * other.num_states
        common_labels = self.bool_matrices.keys() & other.bool_matrices.keys()

        for label in common_labels:
            result.bool_matrices[label] = kron(
                self.bool_matrices[label], other.bool_matrices[label], format="dok"
            )

        for s_first, s_first_index in self.state_indexes.items():
            for s_second, s_second_index in other.state_indexes.items():
                new_state = new_state_index = (
                    s_first_index * other.num_states + s_second_index
                )
                result.state_indexes[new_state] = new_state_index

                if s_first in self.start_states and s_second in other.start_states:
                    result.start_states.add(new_state)

                if s_first in self.final_states and s_second in other.final_states:
                    result.final_states.add(new_state)

        return result

    def _create_boolean_matrices(self, automaton: NondeterministicFiniteAutomaton):
        bool_matrices = {}
        for s_from, trans in automaton.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    index_from = self.state_indexes[s_from]
                    index_to = self.state_indexes[s_to]
                    if label not in bool_matrices:
                        bool_matrices[label] = dok_matrix(
                            (self.num_states, self.num_states), dtype=bool
                        )
                    bool_matrices[label][index_from, index_to] = True

        return bool_matrices
