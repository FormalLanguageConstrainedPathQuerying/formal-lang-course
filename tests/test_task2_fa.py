from pyformlang.finite_automaton import Symbol

from project.task2_fa import regex_to_dfa


class TestRegexToDfa:
    def test_regex_to_dfa_1(self):
        dfa = regex_to_dfa("a|b|c*")

        assert dfa.accepts("a")
        assert dfa.accepts("ccc")
        assert dfa.accepts("")
        assert not dfa.accepts("abab")
        assert not dfa.accepts("aaaa")

    def test_regex_to_dfa_2(self):
        dfa = regex_to_dfa("abc|d")

        assert dfa.accepts([Symbol("abc")])
        assert dfa.accepts([Symbol("d")])
        assert not dfa.accepts([Symbol("b")])
        assert not dfa.accepts("")
