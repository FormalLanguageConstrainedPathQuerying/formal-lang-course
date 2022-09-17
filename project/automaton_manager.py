from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.finite_automaton.finite_automaton import to_state
from pyformlang.regular_expression import Regex


class AutomatonManager:
    @staticmethod
    def create_min_dfa_from_regex(pattern: str) -> DeterministicFiniteAutomaton:
        regex = Regex(pattern)
        fa = regex.to_epsilon_nfa()
        if not fa.is_deterministic():
            fa = fa.to_deterministic()
        return fa.minimize()

    @staticmethod
    def create_nfa_from_graph(
        graph: MultiDiGraph, start_states: set = None, final_states: set = None
    ) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        [
            nfa.add_transition(State(u), Symbol(edge["label"]), State(v))
            for (u, v, edge) in graph.edges.data()
        ]

        start_states = (
            start_states
            if start_states is not None
            else set(map(lambda x: to_state(x), graph.nodes))
        )
        final_states = (
            final_states
            if final_states is not None
            else set(map(lambda x: to_state(x), graph.nodes))
        )

        [nfa.add_start_state(state) for state in start_states]
        [nfa.add_final_state(state) for state in final_states]

        return nfa
