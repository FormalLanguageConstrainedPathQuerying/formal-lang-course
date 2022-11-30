import networkx as nx
import pytest

from project import rpq
from tests.utils import get_data, dot_to_graph


@pytest.mark.parametrize(
    "graph, query, starts, finals, expected",
    get_data(
        "test_rpq",
        lambda d: (
            dot_to_graph(d["graph"]),
            d["query"],
            d["starts"],
            d["finals"],
            {tuple(pair) for pair in d["expected"]},
        ),
    ),
)
def test_rpq_by_bfs_for_each(
    graph: nx.Graph,
    query: str,
    starts: set | None,
    finals: set | None,
    expected: set[tuple],
):
    actual = rpq.rpq_by_bfs(
        graph, query, starts, finals, mode=rpq.BfsMode.FIND_REACHABLE_FOR_EACH_START
    )

    assert actual == expected
