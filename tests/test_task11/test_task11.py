import pytest
from pyformlang import cfg as c

from project.cfpq import tensor_cfpq
from tests.utils import get_data, dot_to_graph
import networkx as nx


@pytest.mark.parametrize(
    "graph, query, start_nodes, final_nodes, start_var, expected",
    get_data(
        "test_cfpq",
        lambda d: (
            dot_to_graph(d["graph"]),
            d["query"],
            d["start_nodes"],
            d["final_nodes"],
            d["start_var"] if d["start_var"] is not None else "S",
            {(triple[0], c.Variable(triple[1]), triple[2]) for triple in d["expected"]},
        ),
    ),
)
def test_cfpq(
    graph: nx.Graph,
    query: str,
    start_nodes: set | None,
    final_nodes: set | None,
    start_var: str,
    expected: set[tuple],
):
    actual = tensor_cfpq(graph, query, start_nodes, final_nodes, start_var)
    assert actual == expected
