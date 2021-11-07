import pytest

from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.grammars.ecfg import ECFG
from project.utils.automata_utils import transform_regex_to_dfa


@pytest.mark.parametrize(
    "cfg, exp_ecfg_productions",
    [
        (
            """
                S -> epsilon
                """,
            {Variable("S"): Regex("$")},
        ),
        (
            """
                S -> a S b S
                S -> epsilon
                """,
            {Variable("S"): Regex("(a S b S) | $")},
        ),
        (
            """
                S -> i f ( C ) t h e n { ST } e l s e { ST }
                C -> t r u e | f a l s e
                ST -> p a s s | S
                """,
            {
                Variable("S"): Regex("i f ( C ) t h e n { ST } e l s e { ST }"),
                Variable("C"): Regex("t r u e | f a l s e"),
                Variable("ST"): Regex("p a s s | S"),
            },
        ),
    ],
)
def test_ecfg_productions(cfg, exp_ecfg_productions):
    ecfg = ECFG.from_pyformlang_cfg(CFG.from_text(cfg))
    ecfg_productions = ecfg.productions
    assert all(
        transform_regex_to_dfa(str(p.body)).is_equivalent_to(
            transform_regex_to_dfa(str(exp_ecfg_productions[p.head]))
        )
        for p in ecfg_productions
    ) and len(ecfg_productions) == len(exp_ecfg_productions)
