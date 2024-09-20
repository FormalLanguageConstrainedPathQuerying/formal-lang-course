from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
)
from typing import Set
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    eps_nfa = Regex(regex).to_epsilon_nfa()
    dfa = eps_nfa.to_deterministic()
    return dfa.minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    graph_nodes = graph.nodes
    nfa = EpsilonNFA.from_networkx(graph).remove_epsilon_transitions()

    if len(start_states) == 0:
        start_states = graph_nodes

    if len(final_states) == 0:
        final_states = graph_nodes

    for state in start_states:
        nfa.add_start_state(State(state))

    for state in final_states:
        nfa.add_final_state(State(state))
    return nfa
