import pytest

from project.ecfg import *
from tests.utils import check_automatons_are_equivalent


@pytest.mark.parametrize(
    "corresponding_ecfg_as_text",
    [
        """
        """,
        """
        S -> a | b
        """,
        """
        S -> (a | b)* | c
        """,
        """
        S -> (d*) | (a b c)
        """,
    ],
)
def test_minimize_rsm(corresponding_ecfg_as_text):
    rsm = ECFG.from_text(corresponding_ecfg_as_text).to_rsm()
    minimized = rsm.minimize()
    assert all(
        check_automatons_are_equivalent(
            automaton,
            automaton.minimize(),
        )
        for automaton in minimized.boxes.values()
    )
