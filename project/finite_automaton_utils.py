from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    regex = Regex(regex)
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int] = None, final_states: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton().from_networkx(graph)
    for state in (
        [state for state in nfa.states]
        if start_states is None
        else [State(state) for state in start_states]
    ):
        nfa.add_start_state(state)
    for state in (
        [state for state in nfa.states]
        if final_states is None
        else [State(state) for state in start_states]
    ):
        nfa.add_final_state(state)

    return nfa
