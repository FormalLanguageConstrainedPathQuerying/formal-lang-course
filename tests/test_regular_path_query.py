import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from pyformlang.regular_expression import Regex

from project.graph_utils import regular_path_query
from test_utils import create_graph

testdata = [
    (
        regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1], edges=[(0, "a", 1)])
        ),
        {(State(0), State(1))},
    ),
    (
        regular_path_query(
            Regex("a.b"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
        ),
        {(State(0), State(2))},
    ),
    (
        regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "a", 2)])
        ),
        {(State(0), State(1)), (State(1), State(2)), (State(0), State(2))},
    ),
    (
        regular_path_query(
            Regex("(a.b)|c"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
        ),
        {(State(0), State(2)), (State(0), State(0))},
    ),
    (
        regular_path_query(
            Regex("c*.a.b"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
        ),
        {(State(0), State(2))},
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_regular_path_query(
    actual: set[tuple[any, any]], expected: set[tuple[any, any]]
):
    assert (
        len(actual.difference(expected)) == 0 and len(expected.difference(actual)) == 0
    )
