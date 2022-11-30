from collections import defaultdict

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import dok_matrix, kron

from project.rsm import RSM


class BooleanDecomposition:
    def __init__(
        self,
        state_indices: dict,
        start_states: set,
        final_states: set,
        bool_decomposition: dict,
    ):
        self.state_indices = state_indices
        self.start_states = start_states
        self.final_states = final_states
        self.bool_decomposition = bool_decomposition

    def __and__(self, other: "BooleanDecomposition") -> "BooleanDecomposition":
        inter_labels = self.bool_decomposition.keys() & other.bool_decomposition.keys()
        inter_bool_matrices = {
            label: kron(self.bool_decomposition[label], other.bool_decomposition[label])
            for label in inter_labels
        }
        inter_states_indices = dict()
        inter_start_states = set()
        inter_final_states = set()
        for self_state, self_idx in self.state_indices.items():
            for other_state, other_idx in other.state_indices.items():
                state = State((self_state.value, other_state.value))
                idx = self_idx * len(other.state_indices) + other_idx
                inter_states_indices[state] = idx
                if (
                    self_state in self.start_states
                    and other_state in other.start_states
                ):
                    inter_start_states.add(state)
                if (
                    self_state in self.final_states
                    and other_state in other.final_states
                ):
                    inter_final_states.add(state)
        return BooleanDecomposition(
            inter_states_indices,
            inter_start_states,
            inter_final_states,
            inter_bool_matrices,
        )

    def to_nfa(self) -> EpsilonNFA:
        nfa = EpsilonNFA()
        for label, matrix in self.bool_decomposition.items():
            matrix_as_array = dok_matrix.toarray()
            for state_from, i in self.state_indices.items():
                for state_to, j in self.state_indices.items():
                    if matrix_as_array[i][j]:
                        nfa.add_transitions([(state_from, label, state_to)])

        for state in self.start_states:
            nfa.add_start_state(state)
        for state in self.final_states:
            nfa.add_final_state(state)

        return nfa

    def get_start_states(self) -> set[State]:
        return self.start_states.copy()

    def get_final_states(self) -> set[State]:
        return self.final_states.copy()

    def make_transitive_closure(self) -> dok_matrix:
        transitive_closure = sum(
            self.bool_decomposition.values(),
            start=dok_matrix((len(self.state_indices), len(self.state_indices))),
        )
        cur_nnz = transitive_closure.nnz
        prev_nnz = None

        if not cur_nnz:
            return transitive_closure

        while prev_nnz != cur_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, cur_nnz = cur_nnz, transitive_closure.nnz

        return transitive_closure

    @classmethod
    def from_nfa(cls, nfa: EpsilonNFA) -> "BooleanDecomposition":
        state_to_index = {state: index for index, state in enumerate(nfa.states)}
        return cls(
            state_indices=state_to_index,
            start_states=nfa.start_states.copy(),
            final_states=nfa.final_states.copy(),
            bool_decomposition=cls._create_boolean_matrix_from_nfa(
                nfa=nfa, state_to_index=state_to_index
            ),
        )

    @classmethod
    def from_rsm(cls, rsm: RSM) -> "BooleanDecomposition":
        states, start_states, final_states = set(), set(), set()
        for nonterm, dfa in rsm.boxes.items():
            for s in dfa.states:
                state = State((nonterm, s.value))
                states.add(state)
                if s in dfa.start_states:
                    start_states.add(state)
                if s in dfa.final_states:
                    final_states.add(state)
        states = sorted(states, key=lambda s: s.value)
        state_to_idx = {s: i for i, s in enumerate(states)}
        b_mtx = defaultdict(lambda: dok_matrix((len(states), len(states)), dtype=bool))
        for nonterm, dfa in rsm.boxes.items():
            for state_from, transitions in dfa.to_dict().items():
                for label, states_to in transitions.items():
                    mtx = b_mtx[label.value]
                    states_to = states_to if isinstance(states_to, set) else {states_to}
                    for state_to in states_to:
                        mtx[
                            state_to_idx[State((nonterm, state_from.value))],
                            state_to_idx[State((nonterm, state_to.value))],
                        ] = True
        return cls(
            state_to_idx,
            start_states,
            final_states,
            b_mtx,
        )

    @staticmethod
    def _create_boolean_matrix_from_nfa(
        nfa: EpsilonNFA, state_to_index: dict[State, int]
    ) -> dict[any, dok_matrix]:
        boolean_matrices = defaultdict(
            lambda: dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
        )
        state_from_to_transition = nfa.to_dict()
        for label in nfa.symbols:
            dok_mtx = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
            for state_from, transitions in state_from_to_transition.items():
                states_to = transitions.get(label, set())
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    dok_mtx[state_to_index[state_from], state_to_index[state_to]] = True
            boolean_matrices[label] = dok_mtx
        return boolean_matrices
