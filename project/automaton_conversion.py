from networkx import MultiDiGraph
from typing import Set
import pyformlang.finite_automaton as fa
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> fa.DeterministicFiniteAutomaton:
    enfa = Regex(regex).to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    return dfa


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> fa.NondeterministicFiniteAutomaton:
    nfa = fa.NondeterministicFiniteAutomaton()

    for u, v, data in graph.edges(data=True):
        label = data.get("label")
        nfa.add_transition(fa.State(u), fa.Symbol(label), fa.State(v))

    if start_states == set():
        start_states = set(graph.nodes())
    if final_states == set():
        final_states = set(graph.nodes())

    for state in start_states:
        nfa.add_start_state(fa.State(state))
    for state in final_states:
        nfa.add_final_state(fa.State(state))

    return nfa
