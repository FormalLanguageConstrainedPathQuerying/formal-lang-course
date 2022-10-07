import pytest
from pyformlang.regular_expression import Regex

from project.regular_path_query import bfs_based_regular_path_query
from test_utils import create_graph

testdata_separated = [
    (
        bfs_based_regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1], edges=[(0, "a", 1)]), True, [0]
        ),
        {(0, 1)},
    ),
    (
        bfs_based_regular_path_query(
            Regex("a.b"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
            True,
            [0],
        ),
        {(0, 2)},
    ),
    (
        bfs_based_regular_path_query(
            Regex("a*"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "a", 2)]),
            True,
            [0, 1],
        ),
        {(1, 2), (0, 2), (0, 1)},
    ),
    (
        bfs_based_regular_path_query(
            Regex("(a.b)|c"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 1), (0, "a", 1), (1, "b", 2)]
            ),
            True,
            [0],
        ),
        {(0, 2), (0, 1)},
    ),
    (
        bfs_based_regular_path_query(
            Regex("c*.a.b"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
            True,
            [0],
        ),
        {(0, 2)},
    ),
    (
        bfs_based_regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1], edges=[(0, "a", 1)]), False, [0]
        ),
        {1},
    ),
    (
        bfs_based_regular_path_query(
            Regex("a.b"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
            False,
            [0],
        ),
        {2},
    ),
    (
        bfs_based_regular_path_query(
            Regex("a*"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "a", 2)]),
            False,
            [0, 1],
        ),
        {2},
    ),
    (
        bfs_based_regular_path_query(
            Regex("(a.b)|c"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 1), (0, "a", 1), (1, "b", 2)]
            ),
            False,
            [0],
        ),
        {2, 1},
    ),
    (
        bfs_based_regular_path_query(
            Regex("c*.a.b"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
            False,
            [0],
        ),
        {2},
    ),
]


@pytest.mark.parametrize("actual,expected", testdata_separated)
def test_bfs_based_regular_path_query(actual: set[any], expected: set[any]):
    assert actual == expected
