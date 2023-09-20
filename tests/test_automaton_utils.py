from project.automaton_utils import regex_to_dfa, graph_to_nfa
from pyformlang.finite_automaton import Symbol
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
