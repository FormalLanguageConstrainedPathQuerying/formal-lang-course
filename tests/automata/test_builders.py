from pathlib import Path

import networkx

from project.automata.builders import *


class TestsForDfa:
    def test_is_minimal(self):
        regex = Regex("(a|b)*|d|f|b.c")
        dfa = build_minimal_dfa(regex)
        assert dfa.is_equivalent_to(regex.to_epsilon_nfa())
        assert dfa.is_deterministic()

    def test_correctness(self):
        regex = Regex("(a|b|c)*|c.d.e|f")
        dfa = build_minimal_dfa(regex)

        expected_true = ["abcabcbbbcaa", "cde", "f", "aaaabbbbb"]
        expected_false = ["acbabxyzbabc", "cdef", "ff", "cd", "de"]
        assert all(
            regex.accepts(list(elem)) and dfa.accepts(elem) for elem in expected_true
        )
        assert all(
            not regex.accepts(list(elem)) and not dfa.accepts(elem)
            for elem in expected_false
        )

    def test_not_empty_str(self):
        regex = Regex("a|b|c.d.e")
        dfa = build_minimal_dfa(regex)

        assert not regex.accepts([]) and not dfa.accepts("")

    def test_empty_str(self):
        regex = Regex("$")
        dfa = build_minimal_dfa(regex)

        assert regex.accepts([]) and dfa.accepts("")


class TestsForNfa:
    def test_nfa_from_graph1(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa1.dot"))
        # dfa that accepts string with "ba" suffix
        enfa = build_nfa(graph, start_states={"0"}, final_states={"2"})

        regex = Regex("((a|b|c)*).(b.a)")
        # regex that accepts string with "ba" suffix
        dfa = build_minimal_dfa(regex)

        assert enfa.is_equivalent_to(dfa)

    def test_nfa_from_graph2(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa2.dot"))
        # dfa that accepts string with "abc" prefix
        enfa = build_nfa(graph, start_states={"0"}, final_states={"3"})

        regex = Regex("(a.b.c).(a|b|c)*")
        # regex that accepts string with "abc" prefix
        dfa = build_minimal_dfa(regex)

        assert enfa.is_equivalent_to(dfa)
