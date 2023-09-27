from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
import networkx as nx


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().remove_epsilon_transitions().minimize()


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_nodes: set = set(), final_nodes: set = set()
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if len(start_nodes) == 0:
        start_nodes = graph.nodes
    if len(final_nodes) == 0:
        final_nodes = graph.nodes
    for start_state in start_nodes:
        nfa.add_start_state(State(start_state))
    for final_state in final_nodes:
        nfa.add_final_state(State(final_state))
    return nfa
