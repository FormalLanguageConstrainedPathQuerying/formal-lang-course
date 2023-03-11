import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol

import project  # on import will print something from __init__ file
from project.graph_utils import GraphUtils
from project.finite_automata_converters import FAConverters
from project.querying import (
    query_to_graph,
    intersection_of_finite_automata_with_tensor_mult,
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
    res = query_to_graph(graph, [0, 1], [1, 2], "a|b")
    assert res == {(0, 1), (0, 2)}

    res = query_to_graph(graph, [0, 1, 2, 3], [0, 1, 2, 3], "a b")
    assert res == {(1, 2)}


def test_4_query_to_graph():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transition(State("s"), Symbol("b"), State("f"))
    nfa.add_transition(State("s"), Symbol("b"), State("m"))
    nfa.add_transition(State("m"), Symbol("c"), State("f"))
    nfa.add_transition(State("m"), Symbol("b"), State("m"))
    nfa.add_transition(State("m"), Symbol("a"), State("s"))

    res = query_to_graph(nfa.to_networkx(), ["s"], ["f"], "(b a b)|b")
    assert res == {("s", "f")}

    res = query_to_graph(nfa.to_networkx(), ["s", "m"], ["f"], "(b a b) | b c*")
    assert res == {("s", "f"), ("m", "f")}
