import pytest
from pyformlang.finite_automaton import EpsilonNFA
from scipy.sparse import csr_array

from project.bool_decomp import BoolDecomp

from tests.utils import (
    get_data,
    _dict_to_nfa_state_info,
    _dict_to_adjs,
    _check_adjs_are_equal,
    dot_to_nfa,
)


@pytest.mark.parametrize(
    "states1, adjs1, states2, adjs2, expected_states",
    get_data(
        "test_intersect",
        lambda d: (
            [_dict_to_nfa_state_info(st) for st in d["states1"]],
            _dict_to_adjs(d["adjs1"]),
            [_dict_to_nfa_state_info(st) for st in d["states2"]],
            _dict_to_adjs(d["adjs2"]),
            [
                BoolDecomp.StateInfo(tuple(st["data"]), st["is_start"], st["is_final"])
                for st in d["expected_states"]
            ],
        ),
    ),
)
def test_states_are_correct(
    states1: list[BoolDecomp.StateInfo],
    adjs1: dict[str, csr_array],
    states2: list[BoolDecomp.StateInfo],
    adjs2: dict[str, csr_array],
    expected_states: list[BoolDecomp.StateInfo],
):
    decomp1 = BoolDecomp(states1, adjs1)
    decomp2 = BoolDecomp(states2, adjs2)
    intersection = decomp1.intersect(decomp2)
    assert intersection.states == expected_states


@pytest.mark.parametrize(
    "states1, adjs1, states2, adjs2, expected_adjs",
    get_data(
        "test_intersect",
        lambda d: (
            [_dict_to_nfa_state_info(st) for st in d["states1"]],
            _dict_to_adjs(d["adjs1"]),
            [_dict_to_nfa_state_info(st) for st in d["states2"]],
            _dict_to_adjs(d["adjs2"]),
            _dict_to_adjs(d["expected_adjs"]),
        ),
    ),
)
def test_adjs_are_correct(
    states1: list[BoolDecomp.StateInfo],
    adjs1: dict[str, csr_array],
    states2: list[BoolDecomp.StateInfo],
    adjs2: dict[str, csr_array],
    expected_adjs: dict[str, csr_array],
):
    decomp1 = BoolDecomp(states1, adjs1)
    decomp2 = BoolDecomp(states2, adjs2)
    intersection = decomp1.intersect(decomp2)
    _check_adjs_are_equal(intersection.adjs, expected_adjs)


@pytest.mark.parametrize(
    "nfa, expected_states",
    get_data(
        "test_from_nfa",
        lambda d: (
            dot_to_nfa(d["graph"]),
            [_dict_to_nfa_state_info(st) for st in d["expected_states"]],
        ),
    ),
)
def test_states_are_correct(
    nfa: EpsilonNFA, expected_states: list[BoolDecomp.StateInfo]
):
    decomp = BoolDecomp.from_nfa(nfa, sort_states=True)
    assert decomp.states == expected_states


@pytest.mark.parametrize(
    "nfa, expected_adjs",
    get_data(
        "test_from_nfa",
        lambda d: (dot_to_nfa(d["graph"]), _dict_to_adjs(d["expected_adjs"])),
    ),
)
def test_adjs_are_correct(nfa: EpsilonNFA, expected_adjs: dict[str, csr_array]):
    decomp = BoolDecomp.from_nfa(nfa, sort_states=True)
    _check_adjs_are_equal(decomp.adjs, expected_adjs)


@pytest.mark.parametrize(
    "adjs, expected_indices",
    get_data(
        "test_closure",
        lambda d: (
            _dict_to_adjs(d["adjs"]),
            {tuple(pair) for pair in d["expected_indices"]},
        ),
    ),
)
def test_closure_is_correct(adjs: dict[str, csr_array], expected_indices: set[tuple]):
    states_num = next(iter(adjs.values())).shape[0] if len(adjs) > 0 else 0
    states = [BoolDecomp.StateInfo(i, True, True) for i in range(states_num)]
    decomp = BoolDecomp(states, adjs)
    actual_indices = decomp.transitive_closure_any_symbol()
    assert set(zip(*actual_indices)) == expected_indices
