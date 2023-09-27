from pathlib import Path

import networkx
from numpy import ndarray, array
from pyformlang.regular_expression import Regex

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import build_minimal_dfa, build_nfa


class TestsForBoolMatrix:
    def test_init(self):
        dfa = build_minimal_dfa(Regex("a.b.c.d|b.c|(d.e)*"))
        bm = BoolMatrix(dfa)

        assert len(bm.states) == len(dfa.states)
        assert bm.states.keys() == dfa.states
        assert bm.matrices.keys() == dfa.symbols

        assert all(
            bm.states[start_state] in bm.start_states
            for start_state in dfa.start_states
        )
        assert all(
            bm.states[final_state] in bm.final_states
            for final_state in dfa.final_states
        )

    def test_to_nfa(self):
        dfa = build_minimal_dfa(Regex("a.b|c|(d.e)*"))
        bm = BoolMatrix(dfa)

        assert bm.to_nfa().is_equivalent_to(dfa)

    def test_intersect(self):
        bm1 = BoolMatrix(build_minimal_dfa(Regex("(a|b|c)*")))
        bm2 = BoolMatrix(build_minimal_dfa(Regex("(b|c|d)*")))
        expected_automata = build_minimal_dfa(Regex("(b|c)*"))

        bm_intersected = bm1.intersect(bm2)
        nfa = bm_intersected.to_nfa()

        assert nfa.is_equivalent_to(expected_automata)

    def test_transitive_closure(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa3.dot"))

        nfa = build_nfa(graph, start_states={"0"}, final_states={"2"})
        bm = BoolMatrix(nfa)
        trc = bm.transitive_closure().toarray()

        expected = {
            "0": {"0": False, "1": True, "2": True, "3": True, "4": True},
            "1": {"0": False, "1": False, "2": True, "3": True, "4": True},
            "2": {"0": False, "1": False, "2": False, "3": True, "4": True},
            "3": {"0": False, "1": False, "2": False, "3": True, "4": False},
            "4": {"0": False, "1": False, "2": False, "3": False, "4": False},
        }

        assert all(
            trc[bm.states[start_state]][bm.states[final_state]] == result
            for start_state, row in expected.items()
            for final_state, result in row.items()
        )
