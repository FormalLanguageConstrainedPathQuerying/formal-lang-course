from project.automaton_utils import *
from project.rpq.automata_intersection_rpq import *
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton
import networkx as nx


def test_collect_labels_set():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(3))
    automaton.add_transition(State(0), Symbol("u"), State(1))
    automaton.add_transition(State(0), Symbol("v"), State(1))
    automaton.add_transition(State(3), Symbol("t"), State(0))
    graph = automaton.to_networkx()
    assert collect_labels_set(graph, 0, 1) == {"a", "u", "v"}


def test_collect_labels_set_empty():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(3))
    automaton.add_transition(State(0), Symbol("u"), State(1))
    automaton.add_transition(State(0), Symbol("v"), State(1))
    automaton.add_transition(State(3), Symbol("t"), State(0))
    graph = nx.transitive_closure(automaton.to_networkx(), None)
    assert len(collect_labels_set(graph, 0, 2)) == 0


def test_automata_intersection():
    automaton1 = regex_to_dfa("(a|b).(c|a).(a*)")
    automaton2 = regex_to_dfa("a*")
    intersection = automata_intersection(automaton1, automaton2)
    assert not intersection.accepts([Symbol("a")])
    assert intersection.accepts([Symbol("a"), Symbol("a")])
    assert intersection.accepts([Symbol("a"), Symbol("a"), Symbol("a")])
    assert not intersection.accepts([Symbol("b")])
    assert not intersection.accepts([Symbol("a"), Symbol("c")])
    assert not intersection.accepts([Symbol("b"), Symbol("c")])


def test_reachability_problem1():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(0), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    graph = automaton.to_networkx()
    assert automata_intersection_rpq(graph, "(a|f).(b|d)", {0}, {2, 4}) == {(0, 2)}


def test_reachability_problem2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("d"), State(1))
    automaton.add_transition(State(1), Symbol("c"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(4))
    automaton.add_transition(State(1), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(0), Symbol("c"), State(5))
    graph = automaton.to_networkx()
    assert automata_intersection_rpq(graph, "(c*|d).(c*)", {0}) == {
        (0, 1),
        (0, 2),
        (0, 4),
        (0, 5),
    }


def test_reachability_problem3():
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
