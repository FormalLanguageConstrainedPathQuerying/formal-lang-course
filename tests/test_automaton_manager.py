import pytest

from project.automaton_manager import AutomatonManager
from project.graph_manager import GraphManager
from pyformlang.finite_automaton import State, Symbol
import os
from networkx import nx_pydot, MultiDiGraph
import networkx


def load_expected_graph() -> MultiDiGraph:
    path = os.path.dirname(os.path.abspath(__file__)) + "/res/expected.dot"
    return nx_pydot.read_dot(path)


def test_create_min_dfa_from_regex():
    pattern = "ab | e | a* | (y|t)*"
    dfa = AutomatonManager.create_min_dfa_from_regex(pattern)

    assert dfa.accepts([Symbol("ab")])
    assert dfa.accepts([Symbol("e")])
    assert dfa.accepts([Symbol("a"), Symbol("a"), Symbol("a")])
    assert dfa.accepts([Symbol("y"), Symbol("y"), Symbol("t")])


def test_create_nfa_from_graph1():
    nfa = AutomatonManager.create_nfa_from_graph(load_expected_graph())

    assert nfa.accepts([Symbol("a")])
    assert nfa.accepts([Symbol("b")])
    assert nfa.get_number_transitions() == 7


def test_create_nfa_from_graph2():
    nfa = AutomatonManager.create_nfa_from_graph(
        load_expected_graph(), start_states={2}
    )

    assert nfa.start_states == {2}
    assert nfa.is_final_state(State("0"))
    assert nfa.is_final_state(State("1"))
    assert nfa.is_final_state(State("2"))
    assert nfa.is_final_state(State("3"))
    assert nfa.is_final_state(State("4"))
    assert nfa.is_final_state(State("5"))


def test_create_nfa_from_graph3():
    nfa = AutomatonManager.create_nfa_from_graph(
        load_expected_graph(), final_states={2}
    )

    assert nfa.start_states.__contains__("0")
    assert nfa.start_states.__contains__("3")
    assert nfa.is_final_state(State(2))
    assert not nfa.is_final_state(State(0))


def test_create_nfa_from_graph4():
    nfa = AutomatonManager.create_nfa_from_graph(
        load_expected_graph(), start_states={1}, final_states={2}
    )

    assert nfa.start_states == {1}
    assert nfa.is_final_state(State(2))
    assert not nfa.is_final_state(State(0))


def test_rpq1():
    graph = MultiDiGraph()
    assert AutomatonManager.rpq(graph, "a*") == set()


def test_rpq2():
    sizes = (2, 3)
    labels = ("a", "b")
    graph = GraphManager._GraphManager__create_two_cycle_labeled_graph(sizes, labels)

    query = "a|bb"
    start_nodes = {0}
    final_nodes = {1, 2, 3}
    actual = AutomatonManager.rpq(graph, query, start_nodes, final_nodes)
    expected = {(0, 1)}
    assert actual == expected


def test_rpq_multisource1():
    graph = MultiDiGraph()

    actual = AutomatonManager.rpq_multisource(graph, "a*")
    expected = set()

    assert actual == expected


def test_rpq_multisource2():
    sizes = (2, 3)
    labels = ("a", "b")
    graph = GraphManager._GraphManager__create_two_cycle_labeled_graph(sizes, labels)

    query = "a|bb"
    start_nodes = {0}
    final_nodes = {1, 2, 3}

    actual = AutomatonManager.rpq_multisource(graph, query, start_nodes, final_nodes)
    expected = {1}

    assert actual == expected
