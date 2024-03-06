from networkx import MultiDiGraph

from pyparsing import Set

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex=regex).to_epsilon_nfa().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa: NondeterministicFiniteAutomaton = NondeterministicFiniteAutomaton()

    states = set(graph.nodes())

    final_states = final_states if final_states else states
    start_states = start_states if start_states else states

    for final_state in final_states:
        nfa.add_final_state(final_state)

    for start_state in start_states:
        nfa.add_start_state(start_state)

    nfa.add_transitions([(f, l, t) for f, t, l in graph.edges(data="label")])

    return nfa
