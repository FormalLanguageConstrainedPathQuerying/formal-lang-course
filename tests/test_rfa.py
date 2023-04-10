import pytest

# from project.graph_regular_query import regex2dfa
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG
from project.rfa import RFA


def test_ecfg2rfa():
    src = """
        S -> A B C
        A -> a
        B -> b
        C -> (a | b | S)
        """

    rfa = ECFG.from_text(src).to_rfa()

    expected = {
        Variable("S"): Regex("A B C"),
        Variable("A"): Regex("a"),
        Variable("B"): Regex("b"),
        Variable("C"): Regex("(a | b | S)"),
    }

    for v in expected.keys():
        assert rfa.dfas[v].is_equivalent_to(expected[v].to_epsilon_nfa())
