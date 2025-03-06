from project.task2 import regex_to_dfa
from pyformlang.finite_automaton import Symbol


def test_regex_to_dfa():
    dfa = regex_to_dfa("abc|d")
    assert dfa.is_deterministic()
    assert dfa.accepts([Symbol("abc")])
    assert dfa.accepts([Symbol("d")])
    assert not dfa.accepts([Symbol("a")])
    assert not dfa.accepts([Symbol("ab")])
    assert not dfa.accepts([Symbol("abcd")])
