from itertools import product

import networkx as nx
import pytest

from project.graph_tools import get_two_cycles
from project.path_querying_tools import regular_str_path_querying


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
    "graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums, mode",
    [
        (
            two_cycles_graph(),
            "a*|b",
            None,
            None,
            set(product(range(4), range(4))).union({(0, 4), (4, 5), (5, 0)}),
            "cpu",
        ),
        (
            two_cycles_graph(),
            "a*|b",
            None,
            None,
            set(product(range(4), range(4))).union({(0, 4), (4, 5), (5, 0)}),
            "gpu",
        ),
        (
            two_cycles_graph(),
            "a*|b",
            {0},
            {1, 2, 3, 4},
            {(0, 1), (0, 2), (0, 3), (0, 4)},
            "cpu",
        ),
        (
            two_cycles_graph(),
            "a*|b",
            {0},
            {1, 2, 3, 4},
            {(0, 1), (0, 2), (0, 3), (0, 4)},
            "gpu",
        ),
        (two_cycles_graph(), "a*|b", {4}, {4, 5}, {(4, 5)}, "cpu"),
        (two_cycles_graph(), "a*|b", {4}, {4, 5}, {(4, 5)}, "gpu"),
        (
            two_cycles_graph(),
            "a.a",
            {0, 1, 2, 3},
            {0, 1, 2, 3},
            {(0, 2), (1, 3), (2, 0), (3, 1)},
            "cpu",
        ),
        (
            two_cycles_graph(),
            "a.a",
            {0, 1, 2, 3},
            {0, 1, 2, 3},
            {(0, 2), (1, 3), (2, 0), (3, 1)},
            "gpu",
        ),
        (two_cycles_graph(), "b", {0}, {0, 1, 2, 3}, set(), "cpu"),
        (two_cycles_graph(), "b", {0}, {0, 1, 2, 3}, set(), "gpu"),
        (two_cycles_graph(), "b*", {0}, {5, 4}, {(0, 5), (0, 4)}, "cpu"),
        (two_cycles_graph(), "b*", {0}, {5, 4}, {(0, 5), (0, 4)}, "gpu"),
        (two_cycles_graph(), "e*|d|zm*", None, None, set(), "cpu"),
        (two_cycles_graph(), "e*|d|zm*", None, None, set(), "gpu"),
        (
            two_cycles_graph(),
            "a*|m",
            None,
            None,
            set((i, j) for i in range(4) for j in range(4)),
            "cpu",
        ),
        (
            two_cycles_graph(),
            "a*|m",
            None,
            None,
            set((i, j) for i in range(4) for j in range(4)),
            "gpu",
        ),
        (empty_graph(), "", None, None, set(), "cpu"),
        (empty_graph(), "", None, None, set(), "gpu"),
        (empty_graph(), "a*|b", None, None, set(), "cpu"),
        (empty_graph(), "a*|b", None, None, set(), "gpu"),
        (acyclic_graph(), "x.y.y", None, None, {(0, 3)}, "cpu"),
        (acyclic_graph(), "x.y.y", None, None, {(0, 3)}, "gpu"),
    ],
)
def test_querying(
    graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums, mode
) -> None:
    actual_reachable_state_nums = regular_str_path_querying(
        graph, regex, start_node_nums, final_node_nums
    )

    assert actual_reachable_state_nums == expected_reachable_state_nums
