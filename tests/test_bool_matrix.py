import pytest
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol

from project.matrix_utils import *


@pytest.fixture
def empty_nfa():
    return EpsilonNFA()


@pytest.fixture
def non_empty_nfa():
    nfa = EpsilonNFA()
    nfa.add_transition(State(0), Symbol("a"), State(0))
    nfa.add_transition(State(0), Symbol("b"), State(1))
    nfa.add_transition(State(1), Symbol("c"), State(1))
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(1))
    return nfa


def test_bool_matrix_from_empty_nfa(empty_nfa):
    mtx = BoolMatrixAutomaton.from_nfa(empty_nfa)
    assert all(
        (
            not mtx.start_states,
            not mtx.final_states,
            not mtx.state_to_idx,
            not mtx.b_mtx,
        )
    )


def test_bool_matrix_from_non_empty_nfa_states(non_empty_nfa):
    mtx = BoolMatrixAutomaton.from_nfa(non_empty_nfa)
    assert all(
        (
            {State(0)} == mtx.start_states,
            {State(1)} == mtx.final_states,
            {State(0): 0, State(1): 1} == mtx.state_to_idx,
        )
    )


def test_bool_matrix_from_non_empty_nfa_matrix(non_empty_nfa):
    mtx = BoolMatrixAutomaton.from_nfa(non_empty_nfa)
    assert all(
        (
            [[True, False], [False, False]] == mtx.b_mtx["a"].toarray().tolist(),
            [[False, True], [False, False]] == mtx.b_mtx["b"].toarray().tolist(),
            [[False, False], [False, True]] == mtx.b_mtx["c"].toarray().tolist(),
        )
    )


def test_bool_matrix_intersection_with_empty(non_empty_nfa, empty_nfa):
    intersection = BoolMatrixAutomaton.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomaton.from_nfa(empty_nfa)
    assert all(
        (
            not intersection.start_states,
            not intersection.final_states,
            not intersection.state_to_idx,
            not intersection.b_mtx,
        )
    )


def test_intersection_with_non_empty_automaton_states(non_empty_nfa):
    intersection = BoolMatrixAutomaton.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomaton.from_nfa(non_empty_nfa)
    assert all(
        (
            {State((0, 0))} == intersection.start_states,
            {State((1, 1))} == intersection.final_states,
            {State((0, 0)): 0, State((0, 1)): 1, State((1, 0)): 2, State((1, 1)): 3}
            == intersection.state_to_idx,
        )
    )


def test_intersection_with_non_empty_automaton_matrix(non_empty_nfa):
    intersection = BoolMatrixAutomaton.from_nfa(
        non_empty_nfa
    ) & BoolMatrixAutomaton.from_nfa(non_empty_nfa)
    for label, values in intersection.b_mtx.items():
        print(label, values.toarray().tolist())
    assert all(
        (
            [
                [True, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
            ]
            == intersection.b_mtx["a"].toarray().tolist(),
            [
                [False, False, False, True],
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
            ]
            == intersection.b_mtx["b"].toarray().tolist(),
            [
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, True],
            ]
            == intersection.b_mtx["c"].toarray().tolist(),
        )
    )


def test_transitive_closure_empty(empty_nfa):
    tc = BoolMatrixAutomaton.from_nfa(empty_nfa).transitive_closure()
    assert not tc.toarray().tolist()


def test_transitive_closure_non_empty(non_empty_nfa):
    tc = BoolMatrixAutomaton.from_nfa(non_empty_nfa).transitive_closure()
    assert [[2, 3], [0, 2]] == tc.toarray().tolist()
