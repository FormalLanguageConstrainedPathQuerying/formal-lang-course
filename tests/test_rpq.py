import pytest
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.rpq import *


@pytest.fixture
def empty_graph():
    return MultiDiGraph()


@pytest.fixture
def non_empty_graph():
    graph = MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 2, label="b")
    graph.add_edge(1, 3, label="c")
    graph.add_edge(1, 3, label="d")
    graph.add_edge(2, 3, label="c")
    graph.add_edge(2, 3, label="d")
    return graph


def test_rpq_empty_graph(empty_graph):
    result = rpq(
        graph=empty_graph,
        query=Regex("abc"),
        start_states=None,
        final_states=None,
    )
    assert not result


def test_rpq_non_empty_graph_one_start_state_one_final_state(non_empty_graph):
    result = rpq(
        graph=non_empty_graph,
        query=Regex("(a|b)(c|d)"),
        start_states={0},
        final_states={3},
    )
    assert {(0, 3)} == result


def test_rpq_non_empty_graph_all_states_are_start_and_final(non_empty_graph):
    result = rpq(
        graph=non_empty_graph,
        query=Regex("(a|b)(c|d)"),
        start_states=None,
        final_states=None,
    )
    assert {(0, 3)} == result
