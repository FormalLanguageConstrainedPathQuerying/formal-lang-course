from pyformlang.regular_expression import Regex

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import build_minimal_dfa


class TestsForBoolMatrix:
    def test_init(self):
        dfa = build_minimal_dfa(Regex("a.b|c|(d.e)*"))
        bm = BoolMatrix(dfa)

        assert bm.to_nfa().is_equivalent_to(dfa)
