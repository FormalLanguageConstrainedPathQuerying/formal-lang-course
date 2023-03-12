from project.graph_utils import create_two_cycles_graph
from project.fa_utils import regex2dfa
from project.graph_regular_query import intersect_nfa, graph_regular_query
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
