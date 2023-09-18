from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
)
import networkx as nx


def build_nfa_from_graph(
    graph: nx.MultiDiGraph, starts_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton(graph.graph)

    if starts_states is None:
        starts_states = graph.nodes
    for node in starts_states:
        nfa.add_start_state(node)

    if final_states is None:
        final_states = graph.nodes
    for node in final_states:
        nfa.add_final_state(node)

    nfa.add_transitions(
        [(u, letters["label"], v) for u, v, letters in graph.edges(data=True)]
    )

    return nfa
