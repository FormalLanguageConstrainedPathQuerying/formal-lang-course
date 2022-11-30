from collections import defaultdict
from typing import Dict, Any

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy import sparse
from pyformlang import finite_automaton
from scipy.sparse import dok_matrix, kron

from project.rsm import RSM


class BooleanDecomposition:
    def __init__(
        self,
        states_num: int,
        state_indices: dict,
        start_states: set,
        final_states: set,
        bool_decomposition: dict,
    ):
        self.states_num = states_num
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
            states_num=inter_states_indices.keys().__len__(),
            state_indices=inter_states_indices,
            start_states=inter_start_states,
            final_states=inter_final_states,
            bool_decomposition=inter_bool_matrices,
        )

    @staticmethod
    def _create_boolean_matrix_from_nfa(
        nfa: EpsilonNFA, state_to_index: Dict[State, int]
    ) -> Dict[Any, dok_matrix]:
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

    @classmethod
    def from_nfa(cls, automaton: finite_automaton.EpsilonNFA):
        state_to_index = {state: index for index, state in enumerate(automaton.states)}
        return cls(
            states_num=len(automaton.states),
            state_indices=state_to_index,
            start_states=automaton.start_states,
            final_states=automaton.final_states,
            bool_decomposition=cls._create_boolean_matrix_from_nfa(
                nfa=automaton, state_to_index=state_to_index
            ),
        )

    def get_states(self):
        return self.state_indices

    def get_start_states(self):
        return self.start_states

    def get_final_states(self):
        return self.final_states

    def get_index(self, state):
        return self.state_indices[state]

    def state_by_index(self, index):
        for state, ind in self.state_indices.items():
            if ind == index:
                return state

    def make_transitive_closure(self):
        if not self.bool_decomposition.values():
            return sparse.dok_matrix((1, 1))

        transitive_closure = sum(self.bool_decomposition.values())
        prev_nnz = transitive_closure.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, curr_nnz = curr_nnz, transitive_closure.nnz

        return transitive_closure

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
            states_num=state_to_idx.keys().__len__(),
            state_indices=state_to_idx,
            start_states=start_states,
            final_states=final_states,
            bool_decomposition=b_mtx,
        )
