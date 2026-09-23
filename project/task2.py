"""Finite automata constructors for regular expressions and labeled graphs."""

from typing import AbstractSet

from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """Build the minimal DFA recognizing `regex` in pyformlang syntax."""
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph,
    start_states: AbstractSet[int] | None = None,
    final_states: AbstractSet[int] | None = None,
) -> NondeterministicFiniteAutomaton:
    """Build an NFA whose states and labeled transitions come from `graph`.

    If either state set is omitted or empty, all graph vertices are used for
    that set. Each graph edge must have a `label` attribute. Multiple graph
    edges with the same source, label, and destination collapse into one NFA
    transition, as they represent the same automaton transition.
    """
    nfa = NondeterministicFiniteAutomaton()

    for source, target, edge_data in graph.edges(data=True):
        nfa.add_transition(source, edge_data["label"], target)

    starts = start_states or set(graph.nodes)
    finals = final_states or set(graph.nodes)
    for state in starts:
        nfa.add_start_state(state)
    for state in finals:
        nfa.add_final_state(state)

    return nfa
