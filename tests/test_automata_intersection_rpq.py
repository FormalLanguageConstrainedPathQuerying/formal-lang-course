from project.automaton_utils import *
from project.rpq.automata_intersection_rpq import *
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton


def test_automata_intersection1():
    automaton1 = str_regex_to_dfa("(a|b).(c|a).(a*)")
    automaton2 = str_regex_to_dfa("a*")
    intersection = automata_intersection(automaton1, automaton2)
    assert not intersection.accepts([Symbol("a")])
    assert intersection.accepts([Symbol("a"), Symbol("a")])
    assert intersection.accepts([Symbol("a"), Symbol("a"), Symbol("a")])
    assert not intersection.accepts([Symbol("b")])
    assert not intersection.accepts([Symbol("a"), Symbol("c")])
    assert not intersection.accepts([Symbol("b"), Symbol("c")])


def test_automata_intersection2():
    automaton1 = str_regex_to_dfa("(ab|ac).(d*)")
    automaton2 = str_regex_to_dfa("((ab)*).(d)")
    intersection = automata_intersection(automaton1, automaton2)
    assert not intersection.accepts([Symbol("ab")])
    assert not intersection.accepts([Symbol("ac")])
    assert intersection.accepts([Symbol("ab"), Symbol("d")])
    assert not intersection.accepts([Symbol("ab"), Symbol("d"), Symbol("d")])


def test_automata_intersection3():
    automaton1 = str_regex_to_dfa("(a*).(b*).(c*)")
    automaton2 = str_regex_to_dfa("b.(c*)")
    intersection = automata_intersection(automaton1, automaton2)
    assert not intersection.accepts([Symbol("a")])
    assert intersection.accepts([Symbol("b")])
    assert not intersection.accepts([Symbol("c")])
    assert intersection.accepts([Symbol("b"), Symbol("c")])
    assert not intersection.accepts([Symbol("b"), Symbol("b"), Symbol("c")])
    assert intersection.accepts([Symbol("b"), Symbol("c"), Symbol("c")])


def test_rpq1():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(0), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    graph = automaton.to_networkx()
    assert automata_intersection_rpq(graph, "(a|f).(b|d)", {0}, {2, 4}) == {(0, 2)}


def test_rpq2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(2), Symbol("d"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("c"), State(6))
    automaton.add_transition(State(3), Symbol("a"), State(5))
    automaton.add_transition(State(5), Symbol("c"), State(6))
    automaton.add_transition(State(2), Symbol("c"), State(7))
    graph = automaton.to_networkx()
    assert automata_intersection_rpq(graph, "(c*|d).(c*)", {2}) == {
        (2, 3),
        (2, 4),
        (2, 6),
        (2, 7),
    }


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
    assert automata_intersection_rpq(graph, "(a*).(b*).(c*).(e*)", {0, 4}) == {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 7),
        (0, 6),
        (4, 5),
        (4, 7),
        (4, 6),
    }
