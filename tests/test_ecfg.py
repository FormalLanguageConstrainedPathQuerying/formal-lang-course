import pytest
from project.ecfg import ECFG
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex


@pytest.mark.parametrize(
    "src, expected",
    [
        ("S -> epsilon", {Variable("S"): Regex("$")}),
        ("S -> epsilon | a S b S", {Variable("S"): Regex("$ | a S b S")}),
    ],
)
def test_productions(src, expected):
    ecfg = ECFG.from_cfg(CFG.from_text(src))
    assert ecfg.productions.keys() == expected.keys()
    for key in expected:
        assert (
            ecfg.productions[key]
            .to_epsilon_nfa()
            .is_equivalent_to(expected[key].to_epsilon_nfa())
        )
