from project.automaton_utils import *
from project.rpq.automata_intersection_rpq import *
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton
from project.graph_utils import get_graph_by_name


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
