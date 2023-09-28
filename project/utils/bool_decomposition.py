from __future__ import annotations

from typing import Set, Dict, Tuple
from scipy.sparse import dok_matrix, kron
from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


class BoolDecompositionOfFA:
    def __init__(
        self,
        *,
        matrices: Dict[str, dok_matrix[bool]] = None,
        state_to_index: Dict[State, int] = None,
        index_to_state: Dict[int, State] = None,
        start_states: Set[State] = None,
        final_states: Set[State] = None,
    ):
        self.matrices = {} if matrices is None else matrices
        self.state_to_index = {} if state_to_index is None else state_to_index
        self.index_to_state = {} if index_to_state is None else index_to_state
        self.start_states = set() if start_states is None else start_states
        self.final_states = set() if final_states is None else final_states

    @staticmethod
    def from_fa(fa: FiniteAutomaton) -> BoolDecompositionOfFA:
        start_states = fa.start_states
        final_states = fa.final_states
        state_to_index, index_to_state = {}, {}
        for index, state in enumerate(fa.states):
            state_to_index[state] = index
            index_to_state[index] = state

        states_count = len(fa.states)
        matrices = {}
        for source, symbol, target in fa:
            symbol = symbol.value
            if symbol not in matrices:
                matrices[symbol] = dok_matrix((states_count, states_count), dtype=bool)
            matrices[symbol][state_to_index[source], state_to_index[target]] = 1

        return BoolDecompositionOfFA(
            matrices=matrices,
            state_to_index=state_to_index,
            index_to_state=index_to_state,
            start_states=start_states,
            final_states=final_states,
        )

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        for state in self.start_states:
            nfa.add_start_state(State(state))
        for state in self.final_states:
            nfa.add_final_state(State(state))
        for symbol, matrix in self.matrices.items():
            for source, target in zip(*matrix.nonzero()):
                nfa.add_transition(
                    self.index_to_state[source],
                    Symbol(symbol),
                    self.index_to_state[target],
                )

        return nfa

    @staticmethod
    def intersection(
        left_bool_fa: BoolDecompositionOfFA, right_bool_fa: BoolDecompositionOfFA
    ) -> BoolDecompositionOfFA:
        intersection = BoolDecompositionOfFA()

        shared_symbols = left_bool_fa.matrices.keys() & right_bool_fa.matrices.keys()
        for symbol in shared_symbols:
            intersection.matrices[symbol] = kron(
                left_bool_fa.matrices[symbol],
                right_bool_fa.matrices[symbol],
                format="dok",
            )

        right_fa_states_count = len(right_bool_fa.state_to_index)
        for left_state, left_index in left_bool_fa.state_to_index.items():
            for right_state, right_index in right_bool_fa.state_to_index.items():
                new_index = left_index * right_fa_states_count + right_index
                new_state = State(new_index)
                intersection.state_to_index[new_state] = new_index
                intersection.index_to_state[new_index] = new_state
                if (
                    left_state in left_bool_fa.start_states
                    and right_state in right_bool_fa.start_states
                ):
                    intersection.start_states.add(new_state)
                if (
                    left_state in left_bool_fa.final_states
                    and right_state in right_bool_fa.final_states
                ):
                    intersection.final_states.add(new_state)

        return intersection

    def transitive_closure(self) -> Set[Tuple[int, int]]:
        sum_matrix = sum(self.matrices.values())

        prev_nnz = sum_matrix.nnz
        curr_nnz = 0
        while prev_nnz != curr_nnz:
            sum_matrix += sum_matrix @ sum_matrix
            prev_nnz, curr_nnz = curr_nnz, sum_matrix.nnz

        return {(row, col) for row, col in zip(*sum_matrix.nonzero())}
