from project.utils import rpq
from project.utils.graph_utils import generate_two_cycles_graph

import networkx as nx

import pytest


@pytest.fixture
def graph():
    return generate_two_cycles_graph("3", "2", "x", "y")


@pytest.fixture
def empty_graph():
    return nx.empty_graph(create_using=nx.MultiDiGraph)


@pytest.fixture
def acyclic_graph():
    graph = nx.MultiDiGraph()
    graph.add_edges_from(
        [(0, 1, {"label": "x"}), (1, 2, {"label": "y"}), (2, 3, {"label": "y"})]
    )
    return graph


def test_full_rpq(graph):
    actual_rpq = rpq.rpq(graph, "x*|y")
    full_rpq = set((i, j) for i in range(4) for j in range(4))

    assert actual_rpq == full_rpq.union({(0, 4), (4, 5), (5, 0)})


def test_empty_graph_rpq(empty_graph):
    actual_rpq = rpq.rpq(empty_graph, "x*|y")
    assert actual_rpq == set()


def test_all_different_labels_query(graph):
    actual_rpq = rpq.rpq(graph, "z*|g")
    assert actual_rpq == set()


def test_acyclic_graph_rpq(acyclic_graph):
    actual_rpq = rpq.rpq(acyclic_graph, "x y y")
    assert actual_rpq == {(0, 3)}


def test_some_different_labels_query(graph):
    actual_rpq = rpq.rpq(graph, "x*|z")
    expected_rpq = set((i, j) for i in range(4) for j in range(4))
    assert actual_rpq == expected_rpq


def test_empty_graph_empty_query(empty_graph):
    actual_rpq = rpq.rpq(empty_graph, "")
    assert actual_rpq == set()


@pytest.mark.parametrize(
    "regex_str,start_nodes,final_nodes,expected_rpq",
    [
        ("x*|y", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("x*|y", {4}, {4, 5}, {(4, 5)}),
        ("y", {0}, {0, 1, 2, 3}, set()),
        ("y*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_rpq(graph, regex_str, start_nodes, final_nodes, expected_rpq):

    actual_rpq = rpq.rpq(graph, regex_str, start_nodes, final_nodes)
    assert actual_rpq == expected_rpq
