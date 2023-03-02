from typing import Set

import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton


def regex_to_min_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Create DFA based on the regex
    :param regex_str: DFA will be created based on this Regex
    :return: DFA
    """
    return Regex(regex_str).to_epsilon_nfa().minimize()


def graph_to_nfa(graph: nx.MultiDiGraph, start_set: Set = None, final_set: Set = None) -> NondeterministicFiniteAutomaton:
    """
    Create NFA based on the given graph
    :param graph: NFA will be created based on this graph
    :param start_set: (optional) set of nodes to be used as start states in NFA
    :param final_set: (optional) set of nodes to be used as final states in NFA
    :return: NFA
    """
    nfa = NondeterministicFiniteAutomaton()
    all_nodes = set(graph.nodes)
    for node_from, node_to, label in graph.edges(data="label"):
        nfa.add_transition(node_from, label, node_to)

    if start_set is None:
        start_set = all_nodes
    for node in start_set:
        nfa.add_start_state(node)

    if final_set is None:
        final_set = all_nodes
    for node in final_set:
        nfa.add_final_state(node)

    return nfa

