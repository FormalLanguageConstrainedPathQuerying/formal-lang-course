import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol

import project  # on import will print something from __init__ file
from project.graph_utils import GraphUtils
from project.querying import (
    query_to_graph_with_kronecker_mult,
    intersection_of_finite_automata_with_tensor_mult,
    find_accessible_nodes,
    query_to_graph_from_any_starts,
    query_to_graph_from_each_starts,
    find_accessible_nodes_foreach_start,
)


def setup_module(module):
    print("query_to_graph setup module")


def teardown_module(module):
    print("query_to_graph teardown module")


def test_1_intersection_of_finite_automata_with_tensor_mult():
    nfa1 = NondeterministicFiniteAutomaton()
    nfa1.add_transition(State("s1"), Symbol("a"), State("f1"))
    nfa1.add_transition(State("s1"), Symbol("b"), State("m1"))
    nfa1.add_transition(State("m1"), Symbol("c"), State("f1"))
    nfa1.add_transition(State("m1"), Symbol("b"), State("m1"))
    nfa1.add_start_state(State("s1"))
    nfa1.add_final_state(State("f1"))

    nfa2 = NondeterministicFiniteAutomaton()
    nfa2.add_transition(State("s2"), Symbol("a"), State("m2"))
    nfa2.add_transition(State("s2"), Symbol("b"), State("f2"))
    nfa2.add_transition(State("m2"), Symbol("c"), State("f2"))
    nfa2.add_transition(State("m2"), Symbol("b"), State("m2"))
    nfa2.add_start_state(State("s2"))
    nfa2.add_final_state(State("f2"))

    inter = intersection_of_finite_automata_with_tensor_mult(nfa1, nfa2)
    inter.minimize()
    assert inter.is_empty()


def test_2_intersection_of_finite_automata_with_tensor_mult():
    nfa1 = NondeterministicFiniteAutomaton()
    nfa1.add_transition(State("s1"), Symbol("a"), State("f1"))
    nfa1.add_transition(State("s1"), Symbol("b"), State("m1"))
    nfa1.add_transition(State("m1"), Symbol("c"), State("f1"))
    nfa1.add_transition(State("m1"), Symbol("b"), State("m1"))
    nfa1.add_transition(State("f1"), Symbol("b"), State("f1"))
    nfa1.add_start_state(State("s1"))
    nfa1.add_final_state(State("f1"))

    nfa2 = NondeterministicFiniteAutomaton()
    nfa2.add_transition(State("s2"), Symbol("b"), State("m2"))
    nfa2.add_transition(State("s2"), Symbol("b"), State("f2"))
    nfa2.add_transition(State("m2"), Symbol("c"), State("f2"))
    nfa2.add_transition(State("m2"), Symbol("b"), State("m2"))
    nfa2.add_transition(State("m2"), Symbol("a"), State("s2"))
    nfa2.add_start_state(State("s2"))
    nfa2.add_final_state(State("f2"))

    inter = intersection_of_finite_automata_with_tensor_mult(nfa1, nfa2)
    inter.minimize()
    assert not inter.is_empty()
    assert not inter.accepts("ab")
    assert not inter.accepts("abb")
    assert inter.accepts("bc")
    assert inter.accepts("bbc")
    assert inter.accepts("bbbbbc")


def test_3_query_to_graph():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    res = query_to_graph_with_kronecker_mult(graph, [0, 1], [1, 2], "a|b")
    assert res == {(0, 1), (0, 2)}

    res = query_to_graph_with_kronecker_mult(graph, [0, 1, 2, 3], [0, 1, 2, 3], "a b")
    assert res == {(1, 2)}


def _get_nfa_for_tests():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transition(State("s"), Symbol("b"), State("f"))
    nfa.add_transition(State("s"), Symbol("b"), State("m"))
    nfa.add_transition(State("m"), Symbol("c"), State("f"))
    nfa.add_transition(State("m"), Symbol("b"), State("m"))
    nfa.add_transition(State("m"), Symbol("a"), State("s"))
    return nfa


def test_4_query_to_graph():
    nfa = _get_nfa_for_tests()
    res = query_to_graph_with_kronecker_mult(
        nfa.to_networkx(), ["s"], ["f"], "(b a b)|b"
    )
    assert res == {("s", "f")}

    res = query_to_graph_with_kronecker_mult(
        nfa.to_networkx(), ["s", "m"], ["f"], "(b a b) | b c*"
    )
    assert res == {("s", "f"), ("m", "f")}


def test_5_find_accessible():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    assert find_accessible_nodes(graph, {0}, "a|b") == {1, 2}
    assert len(find_accessible_nodes(graph, {0}, "a b")) == 0
    assert find_accessible_nodes(graph, {0}, "a a b") == {2}
    assert find_accessible_nodes(graph, {0}, "a a b*") == {0, 2, 3}


def test_6_find_accessible_nodes_foreach_start():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    assert find_accessible_nodes_foreach_start(graph, {0, 1, 2}, "a|b") == {
        0: {1, 2},
        1: {0},
        2: {3},
    }
    assert find_accessible_nodes_foreach_start(graph, {0, 1}, "a b") == {
        0: set(),
        1: {2},
    }
    assert find_accessible_nodes_foreach_start(graph, {0, 1}, "a a b") == {
        0: {2},
        1: set(),
    }
    assert find_accessible_nodes_foreach_start(graph, {0, 1, 2}, "a a* b*") == {
        0: {0, 1, 2, 3},
        1: {0, 1, 2, 3},
        2: set(),
    }


def test_7_query_to_graph_from_any_starts():
    nfa = _get_nfa_for_tests()
    res = query_to_graph_from_any_starts(nfa.to_networkx(), ["s"], ["f"], "(b a b)|b")
    assert res == {"f"}
    res = query_to_graph_from_any_starts(
        nfa.to_networkx(), ["s", "m"], ["f"], "(b a b) | b c*"
    )
    assert res == {"f"}


def test_8_query_to_graph_from_each_starts():
    nfa = _get_nfa_for_tests()
    res = query_to_graph_from_each_starts(nfa.to_networkx(), ["s"], ["f"], "(b a b)|b")
    assert res == {"s": {"f"}}
    res = query_to_graph_from_each_starts(
        nfa.to_networkx(), ["s", "m"], ["f"], "(b a b) | b c*"
    )
    assert res == {"s": {"f"}, "m": {"f"}}
