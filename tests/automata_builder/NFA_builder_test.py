import networkx as nx
from project.automata_builder.NFA_builder import build_nfa_from_graph
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
)


def test_build_nfa_from_graph_default_final_and_start_states():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")

    nfa = build_nfa_from_graph(graph)

    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_start_state(1)
    expected.add_final_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "a", 1)])

    assert nfa.final_states == expected.final_states
    assert nfa.start_states == expected.start_states
    assert nfa.is_equivalent_to(expected)


def test_build_nfa_from_graph():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")
    start_states, final_states = {0}, {1}

    nfa = build_nfa_from_graph(graph, start_states, final_states)

    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "a", 1)])

    assert nfa.final_states == expected.final_states
    assert nfa.start_states == expected.start_states
    assert nfa.is_equivalent_to(expected)
