from scipy.sparse import dok_matrix
from scipy import sparse
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BooleanDecomposition:
    def __init__(self, automaton: NondeterministicFiniteAutomaton = None):
        if automaton is None:
            self.states_num = 0
            self.state_indices = dict()
            self.start_states = set()
            self.final_states = set()
            self.bool_decomposition = dict()
        else:
            self.states_num = len(automaton.states)
            self.state_indices = {
                state: index for index, state in enumerate(automaton.states)
            }
            self.start_states = automaton.start_states
            self.final_states = automaton.final_states
            self.bool_decomposition = self.init_bool_matrices(automaton)

    def get_states(self):
        return self.state_indices.keys()

    def get_start_states(self):
        return self.start_states

    def get_final_states(self):
        return self.final_states

    def init_bool_matrices(self, automaton: NondeterministicFiniteAutomaton):
        bool_matrices = dict()
        nfa_dict = automaton.to_dict()

        for state_from, transition in nfa_dict.items():
            for label, states_to in transition.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = self.state_indices[state_from]
                    index_to = self.state_indices[state_to]
                    if label not in bool_matrices:
                        bool_matrices[label] = sparse.csr_matrix(
                            (self.states_num, self.states_num), dtype=bool
                        )
                    bool_matrices[label][index_from, index_to] = True

        return bool_matrices

    def make_transitive_closure(self):
        if not self.bool_decomposition.values():
            return dok_matrix((1, 1))

        transitive_closure = sum(self.bool_decomposition.values())
        prev_nnz = transitive_closure.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, curr_nnz = curr_nnz, transitive_closure.nnz

        return transitive_closure


def get_intersect_boolean_decomposition(
    self: BooleanDecomposition, other: BooleanDecomposition
):
    intersect = BooleanDecomposition()

    common_symbols = self.bool_decomposition.keys() & other.bool_decomposition.keys()
    for symbol in common_symbols:
        intersect.bool_decomposition[symbol] = sparse.kron(
            self.bool_decomposition[symbol],
            other.bool_decomposition[symbol],
            format="csr",
        )

    for state_fst, state_fst_index in self.state_indices.items():
        for state_snd, state_snd_idx in other.state_indices.items():
            new_state = new_state_idx = (
                state_fst_index * other.states_num + state_snd_idx
            )
            intersect.state_indices[new_state] = new_state_idx

            if state_fst in self.start_states and state_snd in other.start_states:
                intersect.start_states.add(new_state)

            if state_fst in self.final_states and state_snd in other.final_states:
                intersect.final_states.add(new_state)

    return intersect


def decomposition_to_automaton(decomposition: BooleanDecomposition):
    automaton = NondeterministicFiniteAutomaton()

    for label, bool_matrix in decomposition.bool_decomposition.items():
        for state_from, state_to in zip(*bool_matrix.nonzero()):
            automaton.add_transition(state_from, label, state_to)

    for state in decomposition.start_states:
        automaton.add_start_state(State(state))

    for state in decomposition.final_states:
        automaton.add_final_state(State(state))

    return automaton
