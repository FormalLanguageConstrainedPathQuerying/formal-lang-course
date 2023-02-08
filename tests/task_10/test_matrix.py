from typing import Union, Set, Tuple

import networkx as nx
import pytest
from pyformlang.cfg import CFG, Variable

from project.cfpq import cfpq_using_matrix
from project.matrix import matrix
from tests.utils import read_data_from_json, dot_to_graph


@pytest.mark.parametrize(
    "graph, query, starts, finals, start_nonterminal, expected",
    read_data_from_json(
        "test_cfpq_using_matrix",
        lambda data: (
            dot_to_graph(data["graph"]),
            data["query"],
            data["starts"],
            data["finals"],
            data["start_nonterminal"],
            {tuple(pair) for pair in data["expected"]},
        ),
    ),
)
def test_cfpq_by_matrix(
    graph: nx.Graph,
    query: CFG,
    starts: Set[int],
    finals: Set[int],
    start_nonterminal: Union[str, Variable],
    expected,
):
    actual = cfpq_using_matrix(graph, query, starts, finals, start_nonterminal)
    assert actual == expected


@pytest.mark.parametrize(
    "graph, cfg, expected",
    read_data_from_json(
        "test_matrix",
        lambda data: (
            dot_to_graph(data["graph"]),
            CFG.from_text(data["cfg"]),
            {
                (triple["from"], Variable(triple["var"]), triple["to"])
                for triple in data["expected"]
            },
        ),
    ),
)
def test_matrix(graph: nx.Graph, cfg: CFG, expected):
    actual = matrix(graph, cfg)
    assert actual == expected
