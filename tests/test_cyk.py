import pytest
from pyformlang.cfg import CFG

from project.grammars.cyk import cyk


@pytest.mark.parametrize(
    "cfg, words",
    [
        (
            """
                S -> epsilon
                """,
            ["", "epsilon", "abab"],
        ),
        (
            """""",
            ["", "epsilon"],
        ),
        (
            """
                S -> a S b S
                S -> epsilon
                """,
            ["", "aba", "aabbababaaabbb", "abcd", "ab", "aaaabbbb"],
        ),
        (
            """
            S -> A S2 | epsilon
            S1 -> A S2
            S2 -> b | B S1 | S1 S3
            S3 -> b | B S1
            A -> a
            B -> b
            """,
            ["aabbab", "abaa"],
        ),
    ],
)
def test_cyk_equal_pyformlang(cfg, words):
    cfg = CFG.from_text(cfg)
    assert all(cyk(cfg, word) == cfg.contains(word) for word in words)


@pytest.mark.parametrize(
    "cfg, words, accepts",
    [
        (
            """
            S -> epsilon
            S -> ( S )
            S -> S S
            """,
            ["()()", "", "()", ")(", "(("],
            [True, True, True, False, False],
        ),
        (
            """
            S -> b S b b | A
            A -> a A | epsilon
            """,
            ["bbb", "", "babb", "ab"],
            [True, True, True, False],
        ),
    ],
)
def test_cyk_accepts_ground_truth(cfg, words, accepts):
    cfg = CFG.from_text(cfg)
    assert all((cyk(cfg, words[i]) == accepts[i] for i in range(len(words))))
