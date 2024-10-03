from typing import Set
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    NondeterministicFiniteAutomaton,
)
from pyformlang.finite_automaton.state import State
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    epsilon_nfa: EpsilonNFA = Regex(regex).to_epsilon_nfa()
    dfa: DeterministicFiniteAutomaton = epsilon_nfa.to_deterministic()
    return dfa.minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    enfa = EpsilonNFA.from_networkx(graph)
    nfa: NondeterministicFiniteAutomaton = enfa.remove_epsilon_transitions()

    if not start_states:
        start_states = graph
    if not final_states:
        final_states = graph

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))
    return nfa
