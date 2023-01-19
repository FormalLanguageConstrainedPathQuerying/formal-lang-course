from typing import Set, Tuple
import networkx as nx
import pytest
from pyformlang.regular_expression import Regex
from tests.utils import read_data_from_json, dot_to_graph
from project.rpq import rpq


@pytest.mark.parametrize(
    "graph, query, starts, finals, expected",
    read_data_from_json(
        "test_rpq",
        lambda data: (
            dot_to_graph(data["graph"]),
            Regex(data["query"]),
            data["starts"],
            data["finals"],
            {(int(p[0]), int(p[1])) for p in data["expected"]},
        ),
    ),
)
def test_rpq(
    graph: nx.MultiDiGraph,
    query: Regex,
    starts: set,
    finals: set,
    expected: Set[Tuple[int, int]],
):
    actual = rpq(graph, query, starts, finals)
    assert actual == expected
