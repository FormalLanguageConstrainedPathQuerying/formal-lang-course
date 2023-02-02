import pytest
from pyformlang import cfg as c
from copy import deepcopy

from project.ecfg import ECFG
from project.rsm import RSM
from tests.utils import read_data_from_json, eq_automata, dot_to_nfa


@pytest.mark.parametrize(
    "ecfg, expected",
    read_data_from_json(
        "test_rsm",
        lambda data: (
            ECFG.from_cfg(c.CFG.from_text(data["cfg"])),
            RSM(
                c.Variable(data["expected"]["start"]),
                {
                    c.Variable(var): dot_to_nfa(nfa)
                    for var, nfa in data["expected"]["boxes"].items()
                },
            ),
        ),
    ),
)
def test_from_ecfg(ecfg: ECFG, expected: RSM):
    actual = RSM.from_ecfg(ecfg)

    is_equal = False
    if len(actual.boxes) == len(expected.boxes):
        is_equal = all(
            [
                eq_automata(actual.boxes[var], expected.boxes[var])
                for var in expected.boxes.keys()
            ]
        )

    assert is_equal


@pytest.mark.parametrize(
    "original",
    read_data_from_json(
        "test_rsm",
        lambda data: RSM.from_ecfg(ECFG.from_cfg(c.CFG.from_text(data["cfg"]))),
    ),
)
def test_minimize(original: RSM):
    minimized = deepcopy(original).minimize()

    is_equal = False
    if len(minimized.boxes) == len(original.boxes):
        is_equal = all(
            [
                eq_automata(minimized.boxes[var], original.boxes[var])
                for var in original.boxes.keys()
            ]
        )

    assert is_equal
