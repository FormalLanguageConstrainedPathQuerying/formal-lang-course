from typing import List
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
import networkx as nx


def regex_to_min_dfa(regex: str) -> DeterministicFiniteAutomaton:
    regex_obj = Regex(regex)
    enfa = regex_obj.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    min_dfa = dfa.minimize()
    return min_dfa


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_nodes: List[int], final_nodes: List[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if not start_nodes:
        start_nodes = graph.nodes()
    if not final_nodes:
        final_nodes = graph.nodes()
    for node in start_nodes:
        nfa.add_start_state(State(node))
    for node in final_nodes:
        nfa.add_final_state(State(node))

    for start, final, label in graph.edges(data="label"):
        nfa.add_transition(State(start), Symbol(label), State(final))

    return nfa
