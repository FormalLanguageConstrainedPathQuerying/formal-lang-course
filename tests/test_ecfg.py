import pytest
from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG

testdata = [
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> A B C
            A -> a
            B -> b
            C -> c
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("A.B.C"),
                Variable("A"): Regex("a"),
                Variable("B"): Regex("b"),
                Variable("C"): Regex("c"),
            },
        ),
    ),
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> a b c D
            D -> E
            E -> d
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("a.b.c.D"),
                Variable("D"): Regex("E"),
                Variable("E"): Regex("d"),
            },
        ),
    ),
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> A B
            A -> a
            B -> C
            C -> c
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("A.B"),
                Variable("A"): Regex("a"),
                Variable("B"): Regex("C"),
                Variable("C"): Regex("c"),
            },
        ),
    ),
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> A
            A -> a
            B -> b
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("A"),
                Variable("A"): Regex("a"),
                Variable("B"): Regex("b"),
            },
        ),
    ),
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> a b
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("a.b"),
            },
        ),
    ),
    (
        ECFG.from_pyformlang_cfg(
            CFG.from_text(
                """
            S -> S S | a b | $
            """
            )
        ),
        ECFG(
            Variable("S"),
            {
                Variable("S"): Regex("(S.S)|(a.b)|$"),
            },
        ),
    ),
]


def check_ecfg_eq(actual: ECFG, expected: ECFG):
    assert set(actual.productions.keys()) == set(expected.productions.keys())

    for k in actual.productions.keys():
        assert (
            actual.productions[k]
            .to_epsilon_nfa()
            .is_equivalent_to(expected.productions[k].to_epsilon_nfa())
        )

    assert actual.start_variable == expected.start_variable


@pytest.mark.parametrize("actual, expected", testdata)
def test_ecfg_from_pyformlang_cfg(actual: ECFG, expected: ECFG):
    check_ecfg_eq(actual, expected)
