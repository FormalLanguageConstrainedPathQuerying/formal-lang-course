from typing import Set
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    State,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    e_nfa = Regex(regex).to_epsilon_nfa()
    dfa = e_nfa.to_deterministic()
    min_dfa = dfa.minimize()

    return min_dfa


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    if len(start_states) == 0:
        start_states = set(map(int, graph))

    if len(final_states) == 0:
        start_states = set(map(int, graph))

    for state in start_states:
        nfa.add_start_state(State(state))

    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa
