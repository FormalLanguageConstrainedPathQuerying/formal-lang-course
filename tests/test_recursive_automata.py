import pytest
from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG
from project.recursive_automata import RecursiveAutomata

testdata = [
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> A B C
                A -> a
                B -> b
                C -> c
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("A.B.C").to_epsilon_nfa(),
                Variable("A"): Regex("a").to_epsilon_nfa(),
                Variable("B"): Regex("b").to_epsilon_nfa(),
                Variable("C"): Regex("c").to_epsilon_nfa(),
            },
        ),
    ),
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> a b c D
                D -> E
                E -> d
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("a.b.c.D").to_epsilon_nfa(),
                Variable("D"): Regex("E").to_epsilon_nfa(),
                Variable("E"): Regex("d").to_epsilon_nfa(),
            },
        ),
    ),
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> A B
                A -> a
                B -> C
                C -> c
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("A.B").to_epsilon_nfa(),
                Variable("A"): Regex("a").to_epsilon_nfa(),
                Variable("B"): Regex("C").to_epsilon_nfa(),
                Variable("C"): Regex("c").to_epsilon_nfa(),
            },
        ),
    ),
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> A
                A -> a
                B -> b
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("A").to_epsilon_nfa(),
                Variable("A"): Regex("a").to_epsilon_nfa(),
                Variable("B"): Regex("b").to_epsilon_nfa(),
            },
        ),
    ),
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> a b
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("a.b").to_epsilon_nfa(),
            },
        ),
    ),
    (
        RecursiveAutomata.from_ecfg(
            ECFG.from_pyformlang_cfg(
                CFG.from_text(
                    """
                S -> S S | a b | $
                """
                )
            )
        ),
        RecursiveAutomata(
            Variable("S"),
            {
                Variable("S"): Regex("(a.b)|(S.S)|$").to_epsilon_nfa(),
            },
        ),
    ),
]


def check_automata_eq(actual: RecursiveAutomata, expected: RecursiveAutomata):
    assert set(actual.variable_to_automata.keys()) == set(
        expected.variable_to_automata.keys()
    )

    for k in actual.variable_to_automata.keys():
        assert actual.variable_to_automata[k].is_equivalent_to(
            expected.variable_to_automata[k]
        )

    assert actual.start_variable == expected.start_variable


@pytest.mark.parametrize("actual, expected", testdata)
def test_recursive_automata(actual: RecursiveAutomata, expected: RecursiveAutomata):
    check_automata_eq(actual, expected)
