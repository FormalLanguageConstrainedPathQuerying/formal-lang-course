import networkx as nx
import pytest

from project.rpq import rpq
from tests.test_task3.utils import get_data, dot_to_graph


@pytest.mark.parametrize(
    "graph, query, starts, finals, expected",
    get_data(
        "test_rpq",
        lambda data: (
            dot_to_graph(data["graph"]),
            data["query"],
            data["starts"],
            data["finals"],
            {
                tuple(pair)
                for pair in map(
                    lambda values: (int(values[0]), int(values[1])), data["expected"]
                )
            },
        ),
    ),
)
def test_rpq(
    graph,
    query,
    starts,
    finals,
    expected,
):
    actual = rpq(graph, query, starts, finals)
    assert actual == expected
