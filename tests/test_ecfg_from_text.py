import pytest
from pyformlang.cfg import Variable

from project.ecfg import *


@pytest.mark.parametrize(
    "ecfg_as_text, expected_productions",
    [
        (
            "",
            {},
        ),
        (
            "S -> ",
            {Variable("S"): "Empty"},
        ),
        (
            "S -> a | b",
            {Variable("S"): "(a|b)"},
        ),
        (
            """
                A -> (B|c)*
                B -> (A k)
                """,
            {Variable("A"): "((B|c))*", Variable("B"): "(A.k)"},
        ),
    ],
)
def test_ecfg_from_text(ecfg_as_text, expected_productions):
    ecfg = ECFG.from_text(ecfg_as_text)
    productions = {v: str(r) for v, r in ecfg.productions.items()}
    assert productions == expected_productions
