from project.graph_utils import create_two_cycles_graph
from project.fa_utils import regex2dfa, graph2nfa
from project.graph_regular_query import (
    intersect_nfa,
    graph_regular_query,
    get_reachable_vertices,
    bfs_graph_regular_query,
)
from pyformlang.finite_automaton import EpsilonNFA
import cfpq_data
import random
import pytest


def random_regex():
    letters = "abcdefghklmnopqrstuvwxyz "

    left = "l"
    for _ in range(random.randint(2, 10)):
        left += letters[random.randint(0, len(letters) - 1)]
    right = "r"
    for _ in range(random.randint(2, 10)):
        right += letters[random.randint(0, len(letters) - 1)]

    if random.randint(0, 1) == 1:
        left += "*"
    if random.randint(0, 1) == 1:
        right += "*"
    if random.randint(0, 1) == 1:
        right = right + "*"

    if random.randint(0, 1) == 1:
        regex = f"{left}|{right}"
    else:
        regex = f"{left}{right}"

    return regex


def test_intersect_nfa():
    for _ in range(100):
        fa1 = regex2dfa(random_regex())
        fa2 = regex2dfa(random_regex())
        assert fa1.get_intersection(fa2).is_equivalent_to(intersect_nfa(fa1, fa2))


def test_graph_regular_query():
    regex = "(a|b)*"
    graph = create_two_cycles_graph((1, 2), ["a", "b"], "/tmp/tmp")

    assert {(0, 0)} == graph_regular_query(graph, [0], [0], regex)
    assert {(1, 0)} == graph_regular_query(graph, [1], [0], regex)
    assert {(0, 1), (0, 2), (1, 1), (1, 2)} == graph_regular_query(
        graph, [0, 1], [1, 2], regex
    )


def test_get_reachable_vertices():
    regex = "(a|b)*"
    graph = create_two_cycles_graph((1, 2), ["a", "b"], "/tmp/tmp")
    graph_fa = graph2nfa(graph, [], [])

    assert {0, 1, 2, 3} == get_reachable_vertices(regex2dfa(regex), graph_fa, [0])
    assert {0, 1, 2, 3} == get_reachable_vertices(regex2dfa(regex), graph_fa, [1, 2, 3])

    assert {0: {0, 1, 2, 3}} == get_reachable_vertices(
        regex2dfa(regex), graph_fa, [0], True
    )
    assert {
        1: {0, 1, 2, 3},
        2: {0, 1, 2, 3},
        3: {0, 1, 2, 3},
    } == get_reachable_vertices(regex2dfa(regex), graph_fa, [1, 2, 3], True)


def test_bfs_graph_regular_query():
    regex = "(a|b)*"
    graph = create_two_cycles_graph((1, 2), ["a", "b"], "/tmp/tmp")

    assert {0} == bfs_graph_regular_query(graph, [0], [0], regex)
    assert {1} == bfs_graph_regular_query(graph, [0], [1], regex)
    assert {1, 2} == bfs_graph_regular_query(graph, [0, 1], [1, 2], regex)

    assert {0: {0}} == bfs_graph_regular_query(graph, [0], [0], regex, True)
    assert {0: {1}} == bfs_graph_regular_query(graph, [0], [1], regex, True)
    assert {0: {1, 2}, 1: {1, 2}} == bfs_graph_regular_query(
        graph, [0, 1], [1, 2], regex, True
    )
