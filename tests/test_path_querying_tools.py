from collections import namedtuple
from itertools import product

import networkx as nx
import pytest
from cfpq_data import labeled_cycle_graph
from pyformlang.cfg import CFG

from project.graph_tools import get_two_cycles, Graph
from project.path_querying_tools import (
    regular_str_path_querying,
    hellings_context_free_path_querying,
    matrix_context_free_path_querying,
)


def two_cycles_graph() -> nx.MultiDiGraph:
    return get_two_cycles(3, 2).graph


def empty_graph() -> nx.MultiDiGraph:
    return nx.empty_graph(create_using=nx.MultiDiGraph)


def acyclic_graph() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()

    graph.add_edges_from(
        [(0, 1, {"label": "x"}), (1, 2, {"label": "y"}), (2, 3, {"label": "y"})]
    )

    return graph


@pytest.mark.parametrize(
    "graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums",
    [
        (
            two_cycles_graph(),
            "a*|b",
            None,
            None,
            set(product(range(4), range(4))).union({(0, 4), (4, 5), (5, 0)}),
        ),
        (
            two_cycles_graph(),
            "a*|b",
            {0},
            {1, 2, 3, 4},
            {(0, 1), (0, 2), (0, 3), (0, 4)},
        ),
        (two_cycles_graph(), "a*|b", {4}, {4, 5}, {(4, 5)}),
        (
            two_cycles_graph(),
            "a.a",
            {0, 1, 2, 3},
            {0, 1, 2, 3},
            {(0, 2), (1, 3), (2, 0), (3, 1)},
        ),
        (two_cycles_graph(), "b", {0}, {0, 1, 2, 3}, set()),
        (two_cycles_graph(), "b*", {0}, {5, 4}, {(0, 5), (0, 4)}),
        (two_cycles_graph(), "e*|d|zm*", None, None, set()),
        (
            two_cycles_graph(),
            "a*|m",
            None,
            None,
            set((i, j) for i in range(4) for j in range(4)),
        ),
        (empty_graph(), "", None, None, set()),
        (empty_graph(), "a*|b", None, None, set()),
        (acyclic_graph(), "x.y.y", None, None, {(0, 3)}),
    ],
)
def test_querying(
    graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums
) -> None:
    actual_reachable_state_nums = regular_str_path_querying(
        graph, regex, start_node_nums, final_node_nums
    )

    assert actual_reachable_state_nums == expected_reachable_state_nums


@pytest.fixture(
    params=[hellings_context_free_path_querying, matrix_context_free_path_querying]
)
def cfpq(request):
    return request.param


Option = namedtuple(
    "Option", ["start_symbol", "start_node_nums", "final_node_nums", "expected"]
)


@pytest.mark.parametrize(
    "cfg, graph, option",
    [
        (
            """
                A -> a A | epsilon
                B -> b B | b
                """,
            Graph(labeled_cycle_graph(3, "a", verbose=False)),
            [
                Option("A", {0}, {0}, {(0, 0)}),
                Option("A", None, None, set(product(range(3), range(3)))),
                Option("B", None, None, set()),
            ],
        ),
        (
            """
                S -> epsilon
                """,
            Graph(labeled_cycle_graph(4, "b", verbose=False)),
            [
                Option("S", {0, 1}, {0, 1}, {(0, 0), (1, 1)}),
                Option("S", None, None, set((v, v) for v in range(4))),
                Option("B", None, None, set()),
            ],
        ),
        (
            """
                S -> A B
                S -> A S1
                S1 -> S B
                A -> a
                B -> b
                """,
            get_two_cycles(2, 1),
            [
                Option(
                    "S", None, None, {(0, 0), (0, 3), (2, 0), (2, 3), (1, 0), (1, 3)}
                ),
                Option("A", None, None, {(0, 1), (1, 2), (2, 0)}),
                Option("B", None, None, {(3, 0), (0, 3)}),
                Option("S", {0}, {0}, {(0, 0)}),
            ],
        ),
    ],
)
def test_context_free_path_querying(cfpq, cfg, graph, option):
    assert all(
        cfpq(
            graph.graph,
            CFG.from_text(cfg),
            opt.start_symbol,
            opt.start_node_nums,
            opt.final_node_nums,
        )
        == opt.expected
        for opt in option
    )
