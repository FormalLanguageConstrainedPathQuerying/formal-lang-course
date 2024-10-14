from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def get_actual_states(
    states: Set[int], nfa: NondeterministicFiniteAutomaton
) -> list[State]:
    return (
        [state for state in nfa.states]
        if len(states) == 0
        else [State(state) for state in states]
    )


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton().from_networkx(graph)
    for state in get_actual_states(start_states, nfa):
        nfa.add_start_state(state)
    for state in get_actual_states(final_states, nfa):
        nfa.add_final_state(state)
    return nfa
