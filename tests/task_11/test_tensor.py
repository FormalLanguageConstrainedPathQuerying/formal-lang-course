import pytest
from pyformlang import cfg as c

from project.cfpq import cfpq_using_tensor
from tests.utils import read_data_from_json, dot_to_graph
import networkx as nx


@pytest.mark.parametrize(
    "graph, query, start_nodes, final_nodes, start_var, expected",
    read_data_from_json(
        "test_tensor",
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
    start_nodes: set[int] | None,
    final_nodes: set[int] | None,
    start_var: str,
    expected: set[tuple],
):
    actual = cfpq_using_tensor(graph, query, start_nodes, final_nodes, start_var)
    assert actual == expected
