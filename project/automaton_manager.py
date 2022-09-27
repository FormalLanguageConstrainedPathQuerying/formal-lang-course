from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.finite_automaton.finite_automaton import to_state
from pyformlang.regular_expression import Regex

from project.matrix_manager import MatrixManager


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

    @staticmethod
    def rpq(
        graph: MultiDiGraph,
        query: str,
        start_states: set = None,
        final_states: set = None,
    ) -> set:
        nfa = AutomatonManager.create_nfa_from_graph(graph, start_states, final_states)
        dfa = AutomatonManager.create_min_dfa_from_regex(query)

        graph_matrix = MatrixManager.from_nfa_to_boolean_matrix(nfa)
        query_matrix = MatrixManager.from_nfa_to_boolean_matrix(dfa)

        intersected_matrix = MatrixManager.intersect_two_nfa(graph_matrix, query_matrix)
        transitive_closure = MatrixManager.get_transitive_closure(intersected_matrix)

        result = set()
        for source, destination in zip(*transitive_closure.nonzero()):
            if (
                source in intersected_matrix.start_states
                and destination in intersected_matrix.final_states
            ):
                result.add(
                    (
                        source // len(query_matrix.matrix),
                        destination // len(query_matrix.matrix),
                    )
                )

        return result
