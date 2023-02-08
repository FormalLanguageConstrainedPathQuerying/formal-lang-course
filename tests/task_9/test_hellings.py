from typing import Set

import networkx as nx
import pytest
from pyformlang.cfg import CFG, Variable
from project.hellings import hellings, cfpq_using_hellings

from tests.utils import read_data_from_json, dot_to_graph


@pytest.mark.parametrize(
    "graph, cfg, expected",
    read_data_from_json(
        "test_hellings",
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
def test_hellings(graph: nx.Graph, cfg: CFG, expected: Set[tuple]):
    actual = hellings(graph, cfg)

    assert actual == expected


@pytest.mark.parametrize(
    "graph, query, starts, finals, start_nonterminal, expected",
    read_data_from_json(
        "test_cfpq_using_hellings",
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
def test_cfpq_using_hellings(graph, query, starts, finals, start_nonterminal, expected):
    actual = cfpq_using_hellings(graph, query, starts, finals, start_nonterminal)
    assert actual == expected
