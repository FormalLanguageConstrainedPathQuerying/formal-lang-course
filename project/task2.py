from networkx import MultiDiGraph

from pyparsing import Set
from pyformlang.finite_automaton import *

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if not start_states:
        for n in graph.nodes():
            start_states.add(n)
    if not final_states:
        for n in graph.nodes():
            final_states.add(n)

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    for u, v, label in graph.edges(data="label"):
        nfa.add_transition(u, label, v)
    return nfa
