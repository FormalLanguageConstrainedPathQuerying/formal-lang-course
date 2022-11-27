import pytest
from scipy.sparse import csr_array

from project.bool_decomp import BoolDecomp
from tests.utils import get_data, _dict_to_nfa_state_info, _dict_to_adjs


@pytest.mark.parametrize(
    "main_states, main_adjs, constr_states, constr_adjs, expected",
    get_data(
        "test_constr_bfs",
        lambda d: (
            [_dict_to_nfa_state_info(st) for st in d["main_states"]],
            _dict_to_adjs(d["main_adjs"]),
            [_dict_to_nfa_state_info(st) for st in d["constr_states"]],
            _dict_to_adjs(d["constr_adjs"]),
            {end for _, end in d["expected"]},
        ),
    ),
)
def test_not_separated(
    main_states: list[BoolDecomp.StateInfo],
    main_adjs: dict[str, csr_array],
    constr_states: list[BoolDecomp.StateInfo],
    constr_adjs: dict[str, csr_array],
    expected: set[int],
):
    main_decomp = BoolDecomp(main_states, main_adjs)
    constraint_decomp = BoolDecomp(constr_states, constr_adjs)
    actual = main_decomp.constrained_bfs(constraint_decomp)
    assert actual == expected


@pytest.mark.parametrize(
    "main_states, main_adjs, constr_states, constr_adjs, expected",
    get_data(
        "test_constr_bfs",
        lambda d: (
            [_dict_to_nfa_state_info(st) for st in d["main_states"]],
            _dict_to_adjs(d["main_adjs"]),
            [_dict_to_nfa_state_info(st) for st in d["constr_states"]],
            _dict_to_adjs(d["constr_adjs"]),
            {(i, j) for i, j in d["expected"]},
        ),
    ),
)
def test_separated(
    main_states: list[BoolDecomp.StateInfo],
    main_adjs: dict[str, csr_array],
    constr_states: list[BoolDecomp.StateInfo],
    constr_adjs: dict[str, csr_array],
    expected: set[tuple[int, int]],
):
    main_decomp = BoolDecomp(main_states, main_adjs)
    constraint_decomp = BoolDecomp(constr_states, constr_adjs)
    actual = main_decomp.constrained_bfs(constraint_decomp, separated=True)
    assert actual == expected
