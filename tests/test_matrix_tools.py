import sys

import pytest

from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)

from project.matrix_tools import BooleanAdjacencies


@pytest.fixture
def nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [
            (0, "a", 1),
            (0, "a", 2),
            (1, "c", 1),
            (1, "b", 2),
            (2, "d", 3),
            (3, "d", 0),
        ]
    )

    return nfa


def test_boolean_adjacency_symbols(nfa):
    boolean_adjacencies = BooleanAdjacencies(nfa)

    expected_symbols = nfa.symbols
    actual_symbols = set(boolean_adjacencies.boolean_adjacencies.keys())

    assert actual_symbols == expected_symbols


@pytest.mark.parametrize(
    "symbol, adjacency_states",
    [
        ("a", [(0, 1), (0, 2)]),
        ("b", [(1, 2)]),
        ("c", [(1, 1)]),
        ("d", [(2, 3), (3, 0)]),
    ],
)
def test_boolean_adjacency(nfa, symbol, adjacency_states):
    boolean_adjacencies = BooleanAdjacencies(nfa)

    assert all(
        boolean_adjacencies.boolean_adjacencies[symbol][adjacency_state]
        for adjacency_state in adjacency_states
    )


@pytest.mark.parametrize(
    "symbol, expected_nnz",
    [
        ("a", 2),
        ("b", 1),
        ("c", 1),
        ("d", 2),
    ],
)
def test_nonzero_cpu(nfa, symbol, expected_nnz):
    boolean_adjacencies = BooleanAdjacencies(nfa, mode="cpu")

    actual_nnz = boolean_adjacencies.boolean_adjacencies[symbol].nnz

    assert actual_nnz == expected_nnz


@pytest.mark.parametrize(
    "symbol, expected_nnz",
    [
        ("a", 2),
        ("b", 1),
        ("c", 1),
        ("d", 2),
    ],
)
@pytest.mark.skipif(
    not sys.platform == "linux",
    reason="pyCuBool is only supported on Linux platform now",
)
def test_nonzero_gpu(nfa, symbol, expected_nnz):
    boolean_adjacencies = BooleanAdjacencies(nfa, mode="gpu")

    actual_nnz = len(boolean_adjacencies.boolean_adjacencies[symbol].to_list())

    assert actual_nnz == expected_nnz


def test_transitive_closure_cpu(nfa):
    boolean_adjacencies = BooleanAdjacencies(nfa, mode="cpu")

    transitive_closure = boolean_adjacencies.get_transitive_closure()

    assert transitive_closure.sum() == transitive_closure.size


@pytest.mark.skipif(
    not sys.platform == "linux",
    reason="pyCuBool is only supported on Linux platform now",
)
def test_transitive_closure_gpu(nfa):
    boolean_adjacencies = BooleanAdjacencies(nfa, mode="gpu")

    transitive_closure = boolean_adjacencies.get_transitive_closure()

    assert len(transitive_closure.to_list()) == len(
        transitive_closure.to_lists()[0]
    ) and len(transitive_closure.to_list()) == len(transitive_closure.to_lists()[1])


def test_intersection_cpu():
    graph_nfa = NondeterministicFiniteAutomaton()
    graph_nfa.add_transitions(
        [(0, "a", 1), (0, "c", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    graph_nfa.add_start_state(State(0))
    graph_nfa.add_final_state(State(0))
    graph_nfa.add_final_state(State(1))
    graph_nfa.add_final_state(State(2))
    graph_nfa_boolean_adjacencies = BooleanAdjacencies(graph_nfa, mode="cpu")

    query_nfa = NondeterministicFiniteAutomaton()
    query_nfa.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    query_nfa.add_start_state(State(0))
    query_nfa.add_final_state(State(1))
    query_nfa_boolean_adjacencies = BooleanAdjacencies(query_nfa, mode="cpu")

    expected_nfa = DeterministicFiniteAutomaton()
    expected_nfa.add_transitions([(0, "a", 1), (1, "b", 1)])
    expected_nfa.add_start_state(State(0))
    expected_nfa.add_final_state(State(1))

    actual_nfa = graph_nfa_boolean_adjacencies.intersect(
        query_nfa_boolean_adjacencies
    ).to_nfa()

    assert actual_nfa.is_equivalent_to(expected_nfa)


@pytest.mark.skipif(
    not sys.platform == "linux",
    reason="pyCuBool is only supported on Linux platform now",
)
def test_intersection_gpu():
    graph_nfa = NondeterministicFiniteAutomaton()
    graph_nfa.add_transitions(
        [(0, "a", 1), (0, "c", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    graph_nfa.add_start_state(State(0))
    graph_nfa.add_final_state(State(0))
    graph_nfa.add_final_state(State(1))
    graph_nfa.add_final_state(State(2))
    graph_nfa_boolean_adjacencies = BooleanAdjacencies(graph_nfa, mode="gpu")

    query_nfa = NondeterministicFiniteAutomaton()
    query_nfa.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    query_nfa.add_start_state(State(0))
    query_nfa.add_final_state(State(1))
    query_nfa_boolean_adjacencies = BooleanAdjacencies(query_nfa, mode="gpu")

    expected_nfa = DeterministicFiniteAutomaton()
    expected_nfa.add_transitions([(0, "a", 1), (1, "b", 1)])
    expected_nfa.add_start_state(State(0))
    expected_nfa.add_final_state(State(1))

    actual_nfa = graph_nfa_boolean_adjacencies.intersect(
        query_nfa_boolean_adjacencies
    ).to_nfa()

    assert actual_nfa.is_equivalent_to(expected_nfa)
