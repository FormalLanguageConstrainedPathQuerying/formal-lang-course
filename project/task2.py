from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """Return minimized DFA from regular expression string

    Keyword arguments:
    expr -- academic regular expression string;
    """
    dfa = Regex(regex).to_epsilon_nfa()
    return dfa.minimize()


def graph_to_nfa(
        graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    """
    Builds NFA from multi-digraph.
    If start states and/or final states aren't specified, all states will be start/final.
    """

    states = set(graph.nodes())
    labels = set()
    for _, _, label in graph.edges(data="label"):
        if label is not None:
            labels.add(label)

    if not start_states:
        start_states = states
    if not final_states:
        final_states = states

    nfa = NondeterministicFiniteAutomaton()

    for state in states:
        if state in start_states:
            nfa.add_start_state(state)
        if state in final_states:
            nfa.add_final_state(state)

    for source, dest, label in graph.edges(data="label"):
        if label is not None:
            nfa.add_transition(source, label, dest)

    return nfa