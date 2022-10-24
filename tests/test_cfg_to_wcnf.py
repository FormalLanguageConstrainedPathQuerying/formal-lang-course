import pytest
from pyformlang.cfg import CFG, Terminal, Variable, Production

from project.cfg_utils import *


@pytest.mark.parametrize(
    "cfg, expected_productions",
    [
        (
            """
            S -> S
            """,
            set(),
        ),
        (
            """
            A -> b
            """,
            set(),
        ),
        (
            """
            S -> T
            T -> t
            """,
            {Production(Variable("S"), [Terminal("t")])},
        ),
        (
            """
            S ->
            S -> a S b S
            """,
            {
                Production(Variable("S"), []),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("b#CNF#"), [Terminal("b")]),
                Production(Variable("C#CNF#1"), [Variable("S"), Variable("C#CNF#2")]),
                Production(Variable("C#CNF#2"), [Variable("b#CNF#"), Variable("S")]),
            },
        ),
    ],
)
def test_conversion_to_wcnf(cfg, expected_productions):
    cfg_wcnf = cfg_to_wcnf(CFG.from_text(cfg))
    assert cfg_wcnf.productions == expected_productions


@pytest.mark.parametrize(
    "cfg, words",
    [
        (
            """
            S -> S
            """,
            ["", "abc"],
        ),
        (
            """
            S -> T
            T -> t
            """,
            ["", "t", "a"],
        ),
        (
            """
            S ->
            S -> a S b S
            """,
            ["", "ab", "ba", "aabb", "abba", "abab"],
        ),
    ],
)
def test_both_forms_accept_same(cfg, words):
    cfg = CFG.from_text(cfg)
    wcnf = cfg_to_wcnf(cfg)
    assert all(cfg.contains(word) == wcnf.contains(word) for word in words)
