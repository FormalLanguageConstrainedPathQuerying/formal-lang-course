from __future__ import annotations

from typing import Set, Dict
from scipy.sparse import dok_matrix, kron
from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
import networkx as nx


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

    @staticmethod
    def intersection(
        left_bool_fa: BoolDecompositionOfFA, right_bool_fa: BoolDecompositionOfFA
    ) -> NondeterministicFiniteAutomaton:
        intersection = BoolDecompositionOfFA(
            matrices={}, start_states=set(), final_states=set()
        )

        shared_symbols = left_bool_fa.matrices.keys() & right_bool_fa.matrices.keys()
        for symbol in shared_symbols:
            intersection.matrices[symbol] = kron(
                left_bool_fa.matrices[symbol],
                right_bool_fa.matrices[symbol],
                format="dok",
            )

        intersection.start_states = set(
            left_state * len(left_bool_fa.start_states) * right_state
            for left_state in left_bool_fa.start_states
            for right_state in right_bool_fa.start_states
        )
        intersection.final_states = set(
            left_state * len(left_bool_fa.final_states) * right_state
            for left_state in left_bool_fa.final_states
            for right_state in right_bool_fa.final_states
        )

        return intersection.to_nfa()

    @staticmethod
    def transitive_closure(nfa: NondeterministicFiniteAutomaton) -> nx.MultiDiGraph:
        graph = nfa.to_networkx()
        return nx.transitive_closure(graph)
