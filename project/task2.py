from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
import networkx as nx


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    nfa = Regex(regex).to_epsilon_nfa()
    dfa = nfa.minimize()

    return dfa


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_states: set[int], final_states: set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton().from_networkx(graph)
    nodes = set(graph.nodes)
    start_states = start_states if start_states else nodes
    final_states = final_states if final_states else nodes

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa
