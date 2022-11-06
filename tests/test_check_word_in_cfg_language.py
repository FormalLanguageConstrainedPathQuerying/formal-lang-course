import pytest
from pyformlang.cfg import CFG

from project.cfg_utils import check_word_in_cfg_language

testdata = [
    (
        CFG.from_text(
            """
        S -> A B C
        A -> a
        B -> b
        C -> c
        """
        ),
        "abc",
        True,
    ),
    (
        CFG.from_text(
            """
        S -> a b c D
        D -> E
        E -> d
        """
        ),
        "abc",
        False,
    ),
    (
        CFG.from_text(
            """
        S -> A B
        A -> a
        B -> C
        C -> c
        """
        ),
        "ac",
        True,
    ),
    (
        CFG.from_text(
            """
        S -> A
        A -> a
        B -> b
        """
        ),
        "",
        False,
    ),
    (
        CFG.from_text(
            """
        S -> S S | a b | $
        """
        ),
        "",
        True,
    ),
    (
        CFG.from_text(
            """
        S -> S S | a b | $
        """
        ),
        "abab",
        True,
    ),
]


@pytest.mark.parametrize("cfg,word,result", testdata)
def test_check_word_in_cfg_language(cfg: CFG, word: str, result: bool):
    assert result == check_word_in_cfg_language(cfg, word)
