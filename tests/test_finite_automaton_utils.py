import os
import random

import networkx as nx
from pyformlang.finite_automaton import Symbol, DeterministicFiniteAutomaton

from project.finite_automaton_utils import regex_to_dfa, graph_to_nfa
from project.graph_utils import create_two_cycles_graph_and_write_to_dot


class TestRegexToDfa:
    @staticmethod
    def str_to_symbols(string: str) -> list[Symbol]:
        return [Symbol(c) for c in string]

    def test_empty(self):
        dfa = regex_to_dfa("")
        assert dfa.is_deterministic()
        assert dfa.is_empty()

    def test_one_symbol(self):
        dfa = regex_to_dfa("a")
        assert dfa.accepts([Symbol("a")])
        assert not dfa.accepts([Symbol("ab")])

    def test_union(self):
        dfa = regex_to_dfa("ab|c+dc")
        assert dfa.accepts([Symbol("ab")])
        assert dfa.accepts([Symbol("c")])
        assert dfa.accepts([Symbol("dc")])
        assert not dfa.accepts([Symbol("abcdc")])

    def test_kleene_star(self):
        dfa = regex_to_dfa("a*")
        word = ""
        for i in range(10):
            assert dfa.accepts(self.str_to_symbols(word))
            word += "a"

    def test_kleene_star2(self):
        dfa = regex_to_dfa("a*b*")
        word = ""
        for i in range(10):
            for j in range(10):
                assert dfa.accepts(self.str_to_symbols(word))
                word += "b"
            word = "a" + word

    def test_groups(self):
        dfa = regex_to_dfa("(a|b)*")
        word = ""
        for i in range(10):
            assert dfa.accepts(self.str_to_symbols(word))
            word += random.choice(["a", "b"])

    def test_epsilon(self):
        dfa = regex_to_dfa("epsilon")
        assert dfa.accepts([])

    def test_epsilon2(self):
        dfa = regex_to_dfa("$")
        assert dfa.accepts([])


class TestGraphToNfa:
    test_path = "aboba.dot"

    # everything else is tested by auto test
    def test_task1_function(self):
        create_two_cycles_graph_and_write_to_dot(1, 1, ("5", "2"), self.test_path)
        nfa = graph_to_nfa(nx.nx_pydot.read_dot(self.test_path), set(), set())
        assert not nfa.is_deterministic()
        assert nfa.accepts([Symbol("5")])
        assert nfa.accepts([Symbol("2")])
        os.remove(self.test_path)
