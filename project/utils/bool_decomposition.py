from __future__ import annotations

from typing import Set, Dict
from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


class BoolDecompositionOfFA:
    def __init__(
        self,
        matrices: Dict[str, dok_matrix[bool]],
        *,
        start_states: Set[int],
        final_states: Set[int],
    ):
        self.matrices = matrices
        self.start_states = start_states
        self.final_states = final_states

    @staticmethod
    def from_fa(fa: FiniteAutomaton) -> BoolDecompositionOfFA:
        start_states = fa.start_states
        final_states = fa.final_states

        shape = len(fa.states)
        matrices = {}

        for source, symbol, target in fa:
            if symbol not in matrices:
                matrices[symbol] = dok_matrix((shape, shape), dtype=bool)
            matrices[symbol][source, target] = True

        return BoolDecompositionOfFA(
            matrices, start_states=start_states, final_states=final_states
        )

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        for state in self.start_states:
            nfa.add_start_state(State(state))
        for state in self.final_states:
            nfa.add_final_state(State(state))
        for symbol, matrix in self.matrices.items():
            for source, target in matrix.nonzero():
                nfa.add_transition(State(source), Symbol(symbol), State(target))

        return nfa
