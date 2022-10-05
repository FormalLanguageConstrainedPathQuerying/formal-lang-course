import networkx as nx
import pytest
from pyformlang.regular_expression import Regex

from project.rpq_bfs import rpq_bfs
from tests.utils import get_data, dot_to_graph


def list_of_pairs_to_set(list) -> set:
    acc = set()
    for pair in list:
        acc.add((pair[0], pair[1]))
    return acc


@pytest.mark.parametrize(
    "graph, regex, starts, finals, expected, mode",
    get_data(
        "test_rpq_bfs",
        lambda data: (
            dot_to_graph(data["graph"]),
            data["regex"],
            set(data["starts"]),
            set(data["finals"]),
            set(data["expected"])
            if not data["for_each"]
            else list_of_pairs_to_set(data["expected"]),
            data["for_each"],
        ),
    ),
)
def test_rpq_bfs(graph: nx.MultiDiGraph, regex, starts, finals, expected, mode):
    assert rpq_bfs(graph, Regex(regex), starts, finals, mode) == expected
