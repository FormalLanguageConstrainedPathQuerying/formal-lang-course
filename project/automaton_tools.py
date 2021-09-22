from typing import Set

import networkx as nx
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex

__all__ = ["get_min_dfa", "get_nfa"]


def get_min_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """
    Based on a regular expression given as a string, builds an Deterministic Finite Automaton.

    Parameters
    ----------
    regex: str
        The string representation of a regular expression

    Returns
    -------
    DeterministicFiniteAutomaton
        Deterministic Finite Automaton equivalent to a given regular expression as a string

    Raises
    ------
    MisformedRegexError
        If given as string regular expression has an irregular format
    """

    re = Regex(regex)
    e_nfa = re.to_epsilon_nfa()
    min_dfa = e_nfa.minimize()

    return min_dfa


def get_nfa(
    graph: nx.MultiDiGraph, start_nodes: Set[int] = None, final_nodes: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    """
    Generates an Nondeterministic Finite Automaton for a specified graph and start or final nodes.

    If start_nodes or final_nodes are not specified, all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph to generating an Nondeterministic Finite Automaton from it
    start_nodes: Set[int], default = None
        Set of start nodes to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_nodes: Set[int], default = None
        Set of final nodes to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    NondeterministicFiniteAutomaton
        Nondeterministic Finite Automaton equivalent to a specified graph

    Raises
    ------
    ValueError
        If non-existent in the specified graph node is used
    """

    if not start_nodes:
        start_nodes = set(graph.nodes)

    if not final_nodes:
        final_nodes = set(graph.nodes)

    if not start_nodes.issubset(set(graph.nodes)):
        raise ValueError(
            f"Non-existent start nodes in the graph: "
            f"{start_nodes.difference(set(graph.nodes))}"
        )

    if not final_nodes.issubset(set(graph.nodes)):
        raise ValueError(
            f"Non-existent final nodes in the graph: "
            f"{final_nodes.difference(set(graph.nodes))}"
        )

    nfa = NondeterministicFiniteAutomaton()

    for node in graph.nodes:
        nfa.states.add(State(node))

    for node_from, node_to in graph.edges():
        edge_label = graph.get_edge_data(node_from, node_to)[0]["label"]
        nfa.add_transition(node_from, edge_label, node_to)

    for start_node in start_nodes:
        start_state = list(nfa.states)[start_node]
        nfa.add_start_state(start_state)

    for final_node in final_nodes:
        final_state = list(nfa.states)[final_node]
        nfa.add_final_state(final_state)

    return nfa
