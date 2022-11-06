import pytest
from pyformlang.cfg import CFG

from project.cyk import *


@pytest.mark.parametrize(
    "cfg_as_text, words_in_grammar, words_not_in_grammar",
    [
        (
            """
            S ->
            """,
            [""],
            ["a", "b", "aa", "bb"],
        ),
        (
            """
            S ->
            S -> a S b S
            """,
            ["", "ab", "aabb", "abab"],
            ["a", "b", "aa", "bb", "aba", "bab"],
        ),
        (
            """
            S -> 0 | 1
            S -> ( S )
            S -> S + S
            """,
            ["0", "1", "1+1", "(1+0)+1"],
            ["", "2", "(", "1)", "(1+0", "1++1"],
        ),
    ],
)
def test_cyk(cfg_as_text, words_in_grammar, words_not_in_grammar):
    cfg = CFG.from_text(cfg_as_text)
    assert all(cyk(s, cfg) for s in words_in_grammar) and all(
        not cyk(s, cfg) for s in words_not_in_grammar
    )
