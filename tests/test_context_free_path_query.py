import pytest
from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.context_free_path_query import context_free_path_query, Algorithm
from tests.test_utils import create_graph

testdata = [
    (
        (
            CFG.from_text(
                """
                S -> A B
                A -> a
                B -> b
            """
            ),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
        ),
        {(0, 2)},
    ),
    (
        (
            CFG.from_text(
                """
                S -> $
            """
            ),
            create_graph(nodes=[0, 1], edges=[(0, "a", 1), (1, "b", 0)]),
        ),
        {(0, 0), (1, 1)},
    ),
    (
        (
            CFG.from_text(
                """
                S -> A B C
                A -> a
                B -> b
                C -> c
            """
            ),
            create_graph(
                nodes=[0, 1, 2, 3], edges=[(0, "a", 1), (1, "b", 2), (2, "c", 3)]
            ),
        ),
        {(0, 3)},
    ),
    (
        (
            CFG.from_text(
                """
                S -> A B C | S S | s
                A -> a
                B -> b
                C -> c
            """
            ),
            create_graph(
                nodes=[0, 1, 2, 3],
                edges=[(0, "s", 0), (0, "a", 1), (1, "b", 2), (2, "c", 3)],
            ),
        ),
        {(0, 3), (0, 0)},
    ),
    (
        (
            CFG.from_text(
                """
                S -> A B | S S
                A -> a | $
                B -> b
            """
            ),
            create_graph(
                nodes=[0, 1, 2, 3, 4],
                edges=[(0, "a", 1), (1, "b", 2), (2, "a", 3), (3, "b", 4)],
            ),
        ),
        {(0, 4), (2, 4), (1, 2), (3, 4), (1, 4), (0, 2)},
    ),
]


@pytest.mark.parametrize("actual_data, expected", testdata)
def test_context_free_path_query_hellings(
    actual_data: tuple[CFG, MultiDiGraph], expected: set[tuple[any, any]]
):
    cfg, graph = actual_data
    actual = context_free_path_query(cfg, graph, algorithm=Algorithm.HELLINGS)
    assert actual == expected


@pytest.mark.parametrize("actual_data, expected", testdata)
def test_context_free_path_query_matrix(
    actual_data: tuple[CFG, MultiDiGraph], expected: set[tuple[any, any]]
):
    cfg, graph = actual_data
    actual = context_free_path_query(cfg, graph, algorithm=Algorithm.MATRIX)
    assert actual == expected


@pytest.mark.parametrize("actual_data, expected", testdata)
def test_context_free_path_query_tensor(
    actual_data: tuple[CFG, MultiDiGraph], expected: set[tuple[any, any]]
):
    cfg, graph = actual_data
    actual = context_free_path_query(cfg, graph, algorithm=Algorithm.TENSOR)
    assert actual == expected
