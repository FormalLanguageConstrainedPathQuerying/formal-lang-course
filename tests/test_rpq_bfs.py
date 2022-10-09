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
    graph.add_edge(3, 4, label="e")
    graph.add_edge(4, 5, label="e")
    return graph


def graph_by_word(word: str):
    graph = MultiDiGraph()
    for i, c in enumerate(word):
        graph.add_edge(i, i + 1, label=c)
    return graph


def test_rpq_bfs_empty_graph(empty_graph):
    result = rpq_bfs(
        graph=empty_graph,
        query=Regex("abc"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_ALL_REACHABLE,
    )
    assert not result


def test_rpq_bfs_empty_graph_separated(empty_graph):
    result = rpq_bfs(
        graph=empty_graph,
        query=Regex("abc"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_REACHABLE_FOR_EACH_START_NODE,
    )
    assert not result


def test_rpq_bfs_non_empty_graph_one_start_state_one_final_state(non_empty_graph):
    result = rpq_bfs(
        graph=non_empty_graph,
        query=Regex("(a|b)c(d*)(e*)"),
        start_states={0},
        final_states={3},
        mode=MultipleSourceRpqMode.FIND_ALL_REACHABLE,
    )
    assert result == {3}


def test_rpq_bfs_non_empty_graph_one_start_state_one_final_state_separated(
    non_empty_graph,
):
    result = rpq_bfs(
        graph=non_empty_graph,
        query=Regex("(a|b)c(d*)(e*)"),
        start_states={0},
        final_states={3},
        mode=MultipleSourceRpqMode.FIND_REACHABLE_FOR_EACH_START_NODE,
    )
    assert result == {(0, 3)}


def test_rpq_non_empty_graph_all_states_are_start_and_final(non_empty_graph):
    result = rpq_bfs(
        graph=non_empty_graph,
        query=Regex("(a|b)c(d*)(e*)"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_ALL_REACHABLE,
    )
    assert result == {3, 4, 5}


def test_rpq_non_empty_graph_all_states_are_start_and_final_separated(non_empty_graph):
    result = rpq_bfs(
        graph=non_empty_graph,
        query=Regex("(a|b)c(d*)(e*)"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_REACHABLE_FOR_EACH_START_NODE,
    )
    assert result == {(0, 3), (0, 4), (0, 5)}


def test_rpq_graph_by_word():
    result = rpq_bfs(
        graph=graph_by_word("abababa"),
        query=Regex("(a)(b)(a)"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_ALL_REACHABLE,
    )
    assert result == {3, 5, 7}


def test_rpq_graph_by_word_separated():
    result = rpq_bfs(
        graph=graph_by_word("abababa"),
        query=Regex("(a)(b)(a)"),
        start_states=None,
        final_states=None,
        mode=MultipleSourceRpqMode.FIND_REACHABLE_FOR_EACH_START_NODE,
    )
    assert result == {(0, 3), (2, 5), (4, 7)}
