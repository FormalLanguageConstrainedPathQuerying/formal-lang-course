from project.utils.matrix_utils import BooleanMatrix

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy.sparse import dok_matrix

import pytest


@pytest.fixture
def lhs_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions([(0, "b", 0), (0, "a", 1), (1, "b", 1), (1, "a", 0)])
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(1))

    return nfa


@pytest.fixture
def empty_nfa():
    return NondeterministicFiniteAutomaton()


@pytest.fixture
def nfa_several_labels(lhs_nfa):
    nfa = lhs_nfa.copy()
    nfa.add_transitions([(0, "c", 1), (1, "e", 0)])

    return nfa


@pytest.fixture
def rhs_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [(0, "b", 0), (0, "a", 1), (1, "a", 1), (1, "b", 2), (2, "b", 0)]
    )
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(0))
    nfa.add_final_state(State(1))

    return nfa


@pytest.fixture
def nfa_unordered_states():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions([(115, "a", 991), (-10, "b", 11), (5, "c", 991)])

    return nfa


def test_pyformlang_intersect_default(lhs_nfa, rhs_nfa):
    expected_result = lhs_nfa.get_intersection(rhs_nfa)

    lhs_bm = BooleanMatrix.from_nfa(lhs_nfa)
    rhs_bm = BooleanMatrix.from_nfa(rhs_nfa)

    intersection_bm = lhs_bm.intersect(rhs_bm)
    intersection = intersection_bm.to_nfa()

    assert intersection.is_equivalent_to(expected_result)


def test_pyformlang_intersect_with_several(nfa_several_labels, rhs_nfa):
    expected_result = nfa_several_labels.get_intersection(rhs_nfa)

    lhs_bm = BooleanMatrix.from_nfa(nfa_several_labels)
    rhs_bm = BooleanMatrix.from_nfa(rhs_nfa)

    intersection_bm = lhs_bm.intersect(rhs_bm)
    intersection = intersection_bm.to_nfa()

    assert intersection.is_equivalent_to(expected_result)


def test_intersect_with_empty(lhs_nfa, empty_nfa):

    lhs_bm = BooleanMatrix.from_nfa(lhs_nfa)
    rhs_bm = BooleanMatrix.from_nfa(empty_nfa)

    intersection_bm = lhs_bm.intersect(rhs_bm)
    intersection = intersection_bm.to_nfa()

    assert intersection.is_empty()


def test_to_nfa_from_nfa(lhs_nfa):
    lhs_bm = BooleanMatrix.from_nfa(lhs_nfa)
    expected_nfa = lhs_bm.to_nfa()

    assert lhs_nfa.is_equivalent_to(expected_nfa)


def test_renumbered_keys(nfa_unordered_states):
    nfa_bm = BooleanMatrix.from_nfa(nfa_unordered_states)
    assert nfa_bm.indexed_states.keys() == nfa_unordered_states.states


def test_renumbered_values(nfa_unordered_states):
    nfa_bm = BooleanMatrix.from_nfa(nfa_unordered_states)
    assert sorted(nfa_bm.indexed_states.values()) == [0, 1, 2, 3, 4]


def test_nfa_to_bmatrix(lhs_nfa):
    lhs_bm = BooleanMatrix.from_nfa(lhs_nfa)

    bmatrix = {
        "a": dok_matrix([[0, 1], [1, 0]], dtype=bool),
        "b": dok_matrix([[1, 0], [0, 1]], dtype=bool),
    }

    assert lhs_bm.bmatrix["a"].items() == bmatrix["a"].items()


def test_transitive_closure(lhs_nfa):
    lhs_bm = BooleanMatrix.from_nfa(lhs_nfa)
    tc = dok_matrix([[True, True], [True, True]])

    assert lhs_bm.transitive_closure().toarray().data == tc.toarray().data
