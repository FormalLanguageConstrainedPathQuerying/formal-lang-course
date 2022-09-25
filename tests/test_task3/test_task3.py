import cfpq_data
import networkx as nx
import pytest
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    DeterministicFiniteAutomaton,
)

from project.boolean_decompositon import (
    get_intersect_boolean_decomposition,
    decomposition_to_automaton,
)
from project.rpq import (
    BooleanDecomposition,
    rpq,
)


def test_intersection():
    fa1 = NondeterministicFiniteAutomaton()
    fa1.add_transitions(
        [(0, "a", 1), (0, "b", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    fa1.add_start_state(State(0))
    fa1.add_final_state(State(0))
    fa1.add_final_state(State(1))
    fa1.add_final_state(State(2))

    decomposition1 = BooleanDecomposition(fa1)

    fa2 = NondeterministicFiniteAutomaton()
    fa2.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    fa2.add_start_state(State(0))
    fa2.add_final_state(State(1))

    decomposition2 = BooleanDecomposition(fa2)

    expected = DeterministicFiniteAutomaton()
    expected.add_transitions([(0, "a", 1), (1, "b", 1)])
    expected.add_start_state(State(0))
    expected.add_final_state(State(1))

    intersected = get_intersect_boolean_decomposition(decomposition1, decomposition2)

    fa = decomposition_to_automaton(intersected)

    assert fa.is_equivalent_to(expected)


@pytest.fixture
def two_cycle_graph():
    return cfpq_data.labeled_two_cycles_graph(3, 2, labels=("a", "b"))


@pytest.fixture
def empty_graph():
    return nx.empty_graph(create_using=nx.MultiDiGraph)


@pytest.fixture
def linear_graph():
    graph = nx.MultiDiGraph()
    graph.add_edges_from(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "b"})]
    )

    return graph


@pytest.mark.parametrize(
    "query, start_nodes, final_nodes, expected_rpq",
    [
        (
            "a*|b*",
            None,
            None,
            {
                (4, 0),
                (3, 1),
                (5, 4),
                (0, 2),
                (0, 5),
                (2, 2),
                (1, 0),
                (1, 3),
                (3, 0),
                (4, 5),
                (3, 3),
                (5, 0),
                (0, 1),
                (1, 2),
                (0, 4),
                (2, 1),
                (3, 2),
                (4, 4),
                (5, 5),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 0),
                (2, 3),
            },
        ),
        ("a*|b*", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("a*|b*", {4}, {4, 5}, {(4, 4), (4, 5)}),
        ("b", {0}, {0, 1, 2, 3}, set()),
        ("b*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_rpq(two_cycle_graph, query, start_nodes, final_nodes, expected_rpq):
    actual_rpq = rpq(two_cycle_graph, query, start_nodes, final_nodes)

    assert actual_rpq == expected_rpq


def test_empty_graph_empty_query(empty_graph):
    actual_rpq = rpq(empty_graph, "")
    assert actual_rpq == set()


def test_empty_graph(empty_graph):
    actual_rpq = rpq(empty_graph, "a*|b*")
    assert actual_rpq == set()


def test_linear_graph(linear_graph):
    actual_rpq = rpq(linear_graph, "a b b")
    assert actual_rpq == {(0, 3)}


def test_bad_label_name(linear_graph):
    actual_rpq = rpq(linear_graph, "c|d")
    assert actual_rpq == set()
