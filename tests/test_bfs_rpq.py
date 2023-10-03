from project.automaton_utils import *
from project.rpq.bfs_rpq import *
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton


def test_rpq1():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(0), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a|f).(b|d)", {0}, {2, 4}) == {2}


def test_rpq2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("d"), State(1))
    automaton.add_transition(State(1), Symbol("c"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(4))
    automaton.add_transition(State(1), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(0), Symbol("c"), State(5))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(c*|d).(c*)", {0}) == {1, 2, 4, 5}


def test_rpq3():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("a"), State(5))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a*).(b*).(c*).(e*)", {0}) == {1, 2, 3, 4, 7, 6}


def test_rpq4():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("a"), State(5))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a*).(b*).(c*).(e*)", {4}) == {5, 6, 7}


def test_rpq5():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("a"), State(5))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a*).(b*).(c*).(e*)", {6}) == set()


def test_rpq6():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("a"), State(5))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a*).(b*).(c*).(e*)", {6}) == set()


def test_rpq7():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("d"), State(4))
    automaton.add_transition(State(1), Symbol("c"), State(5))
    automaton.add_transition(State(5), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("d"), State(7))
    automaton.add_transition(State(1), Symbol("a"), State(10))
    automaton.add_transition(State(10), Symbol("a"), State(8))
    automaton.add_transition(State(10), Symbol("b"), State(9))
    automaton.add_transition(State(8), Symbol("b"), State(7))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "a.b", {1, 10}) == {3, 7, 9}


def test_rpq8():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(0), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a|f).(b|d)", {0}, {2, 4}, task_type=2) == {0: {2}}


def test_rpq9():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("d"), State(1))
    automaton.add_transition(State(1), Symbol("c"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(4))
    automaton.add_transition(State(1), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(0), Symbol("c"), State(5))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(c*|d).(c*)", {0}, task_type=2) == {0: {1, 2, 4, 5}}


def test_rpq10():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("a"), State(5))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "(a*).(b*).(c*).(e*)", {0, 4}, task_type=2) == {
        0: {1, 2, 3, 7, 6},
        4: {5, 6, 7},
    }


def test_rpq11():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("d"), State(4))
    automaton.add_transition(State(1), Symbol("c"), State(5))
    automaton.add_transition(State(5), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("d"), State(7))
    automaton.add_transition(State(1), Symbol("a"), State(10))
    automaton.add_transition(State(10), Symbol("a"), State(8))
    automaton.add_transition(State(10), Symbol("b"), State(9))
    automaton.add_transition(State(8), Symbol("b"), State(7))
    automaton.add_transition(State(6), Symbol("c"), State(11))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "a.b", {1, 5, 10}, task_type=2) == {
        1: {3, 9},
        10: {7},
        5: set(),
    }


def test_rpq12():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State("1"), Symbol("a"), State("2"))
    automaton.add_transition(State("2"), Symbol("a"), State("3"))
    automaton.add_transition(State("3"), Symbol("a"), State("4"))
    automaton.add_transition(State("4"), Symbol("a"), State("1"))
    graph = automaton.to_networkx()
    assert bfs_rpq(graph, "a*", {"1"}, task_type=2) == {"1": {"2", "3", "4"}}
