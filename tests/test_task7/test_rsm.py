import pytest
from pyformlang import cfg as c
from copy import deepcopy

from project.ecfg import ECFG
from project.rsm import RSM
from tests.utils import get_data, eq_automata, dot_to_nfa


@pytest.mark.parametrize(
    "ecfg, expected",
    get_data(
        "test_rsm",
        lambda d: (
            ECFG.from_cfg(c.CFG.from_text(d["cfg"])),
            RSM(
                c.Variable(d["expected"]["start"]),
                {
                    c.Variable(var): dot_to_nfa(nfa)
                    for var, nfa in d["expected"]["boxes"].items()
                },
            ),
        ),
    ),
)
def test_correctness_building_of_boxes(ecfg: ECFG, expected: RSM):
    def helper(actual, expected):
        acc = True
        for var in expected.boxes:
            acc = acc and eq_automata(actual.boxes[var], expected.boxes[var])

        return len(actual.boxes) == len(expected.boxes) and acc

    actual = RSM.from_ecfg(ecfg)
    assert helper(actual, expected)


@pytest.mark.parametrize(
    "original",
    get_data(
        "test_rsm",
        lambda d: RSM.from_ecfg(ECFG.from_cfg(c.CFG.from_text(d["cfg"]))),
    ),
)
def test_correctness_for_minimized(original: RSM):
    minimized = deepcopy(original).minimize()

    assert len(minimized.boxes) == len(original.boxes)
    for var in original.boxes:
        assert eq_automata(minimized.boxes[var], original.boxes[var])
