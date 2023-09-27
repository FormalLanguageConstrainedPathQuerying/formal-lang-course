from pyformlang.regular_expression import Regex

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import build_minimal_dfa


class TestsForBoolMatrix:
    def test_init(self):
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
