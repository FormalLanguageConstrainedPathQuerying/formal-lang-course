import pytest
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.ecfg import *
from project.automata import *
from tests.utils import check_automatons_are_equivalent


@pytest.mark.parametrize(
    "cfg_as_text, ecfg_productions_str",
    [
        (
            "",
            {},
        ),
        (
            "S -> ",
            {Variable("S"): ""},
        ),
        (
            """
                S -> a
                S -> a
                """,
            {Variable("S"): "a"},
        ),
        (
            """
                S -> a | b | c
                """,
            {Variable("S"): "((a|b)|c)"},
        ),
    ],
)
def test_cfg_to_ecfg(cfg_as_text, ecfg_productions_str):
    ecfg = ECFG.from_cfg(CFG.from_text(cfg_as_text))
    expected_productions = {v: Regex(r) for v, r in ecfg_productions_str.items()}
    assert len(ecfg.productions) == len(expected_productions)
    assert all(
        check_automatons_are_equivalent(
            regex_to_min_dfa(ecfg.productions[v]),
            regex_to_min_dfa(expected_productions[v]),
        )
        for v in ecfg.productions
    )
