from typing import Hashable, Set

from pyformlang.regular_expression import *
from pyformlang.finite_automaton import *
from networkx import MultiDiGraph


def build_minimal_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """Transforms the regular expression into a minimal DFA

    Parameters
    ----------
    regex : pyformlang.regular_expression.Regex
        The regular expression

    Returns
    ----------
    dfa : pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton
        The minimal DFA

    """
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic().minimize()
    return dfa


def build_nfa(
    graph: MultiDiGraph,
    start_states: set[Hashable] = None,
    final_states: set[Hashable] = None,
) -> NondeterministicFiniteAutomaton:
    """Import a networkx.MultiDiGraph into a finite state automaton. \
    The imported graph requires to have the "label" marks on edges \
    that indicate the transition symbol; OPTIONAL "is_start": bool indicate \
    start states; OPTIONAL "is_final": bool indicate final states.

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The graph representation of the automaton
    start_states: set[Hashable], optional
        A finite set of start states - graph nodes
    final_states: set[Hashable], optional
        A finite set of final states - graph nodes

    Returns
    -------
    enfa :
        A epsilon nondeterministic finite automaton read from the graph

    """
    received_graph = graph.copy()
    if start_states is None and final_states is None:
        for node in graph.nodes(data=False):
            received_graph.nodes[node]["is_start"] = True
            received_graph.nodes[node]["is_final"] = True

    if start_states is not None:
        for node in start_states:
            received_graph.nodes[node]["is_start"] = True

    if final_states is not None:
        for node in final_states:
            received_graph.nodes[node]["is_final"] = True

    enfa = NondeterministicFiniteAutomaton.from_networkx(received_graph)
    return enfa
