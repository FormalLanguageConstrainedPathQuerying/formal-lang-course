import cfpq_data
import networkx as nx
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from project.task2 import graph_to_nfa, regex_to_dfa


def test_regex_to_dfa_is_minimized_and_recognizes_language():
    dfa = regex_to_dfa("(a | b)* c")

    assert isinstance(dfa, DeterministicFiniteAutomaton)
    assert dfa.is_deterministic()
    assert len(dfa.states) == len(dfa.minimize().states)
    assert dfa.accepts(["a", "b", "c"])
    assert dfa.accepts(["c"])
    assert not dfa.accepts(["c", "a"])
    assert not dfa.accepts([])


def test_regex_to_dfa_minimizes_equivalent_expressions():
    first = regex_to_dfa("(a | b)*")
    equivalent = regex_to_dfa("(a | b)* (a | b)*")

    assert first.is_equivalent_to(equivalent)
    assert len(first.states) == len(equivalent.states)


def test_graph_to_nfa_handles_nondeterminism_parallel_edges_and_selected_states():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3, 4])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 2, label="a")
    graph.add_edge(1, 3, label="b")
    graph.add_edge(2, 3, label="c")

    nfa = graph_to_nfa(graph, {0}, {3})

    assert nfa.accepts(["a", "b"])
    assert nfa.accepts(["a", "c"])
    assert not nfa.accepts(["a"])
    assert not nfa.accepts(["b"])
    assert graph.number_of_edges() == 5


def test_graph_to_nfa_supports_cfpq_data_generated_graph():
    graph = cfpq_data.labeled_two_cycles_graph(1, 1, labels=("a", "b"))

    nfa = graph_to_nfa(graph, {0}, {0})

    assert nfa.accepts(["a", "a"])
    assert nfa.accepts(["b", "b"])
    assert not nfa.accepts(["a", "b"])


def test_graph_to_nfa_defaults_empty_state_sets_to_all_vertices():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="x")
    graph.add_node(2)

    nfa = graph_to_nfa(graph, set(), set())

    assert nfa.accepts([])
    assert nfa.accepts(["x"])


def test_graph_to_nfa_can_be_called_without_state_sets():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="edge")

    nfa = graph_to_nfa(graph)

    assert nfa.accepts([])
    assert nfa.accepts(["edge"])


def test_graph_to_nfa_empty_graph_accepts_nothing():
    nfa = graph_to_nfa(nx.MultiDiGraph())

    assert nfa.is_empty()
