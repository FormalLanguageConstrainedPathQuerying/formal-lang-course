from project.automaton_utils import *
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton
from project.graph_utils import get_graph_by_name
import networkx as nx


def test_regex_to_dfa():
    dfa = regex_to_dfa("(a|b).(b|c)")
    assert dfa.accepts([Symbol("a"), Symbol("b")])
    assert dfa.accepts([Symbol("a"), Symbol("c")])
    assert dfa.accepts([Symbol("b"), Symbol("b")])
    assert dfa.accepts([Symbol("b"), Symbol("c")])
    assert not dfa.accepts([Symbol("c"), Symbol("a")])
    assert not dfa.accepts([Symbol("c"), Symbol("b")])
    assert not dfa.accepts([Symbol("b"), Symbol("a")])
    assert len(dfa.states) == 3


def test_graph_to_nfa():
    nfa = graph_to_nfa(get_graph_by_name("atom"), {0, 1}, {5, 7, 8})
    assert nfa.start_states == {0, 1}
    assert nfa.final_states == {5, 7, 8}


def test_graph_to_nfa_empty_sets():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(2), Symbol("d"), State(4))
    graph = automaton.to_networkx()
    nfa = graph_to_nfa(graph)
    assert nfa.start_states == {0, 1, 2, 4}
    assert nfa.final_states == {0, 1, 2, 4}
    assert set(graph.nodes) == set(nfa.states)


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
    graph = automaton_transitive_closure(automaton)
    assert len(collect_labels_set(graph, 0, 2)) == 0


def test_automaton_transitive_closure():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(0))
    automaton.add_transition(State(2), Symbol("d"), State(3))
    automaton.add_transition(State(3), Symbol("f"), State(2))
    adjacency_matrix = nx.adjacency_matrix(automaton_transitive_closure(automaton))
    assert adjacency_matrix.count_nonzero() == 12


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
    assert reachability_problem(graph, "(a|f).(b|d)", {0}, {2, 4}) == {(0, 2)}


def test_reachability_problem2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("d"), State(1))
    automaton.add_transition(State(1), Symbol("c"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(4))
    automaton.add_transition(State(1), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(0), Symbol("c"), State(5))
    graph = automaton.to_networkx()
    assert reachability_problem(graph, "(c*|d).(c*)", {0}) == {
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
    assert reachability_problem(graph, "(a*).(b*).(c*).(e*)", {0, 4}) == {
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
