from itertools import product

import networkx as nx
import sys
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
@pytest.mark.skipif(
    not sys.platform == "linux",
    reason="pyCuBool is only supported on Linux platform now",
)
def test_querying_cpu(
    graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums
) -> None:
    actual_reachable_state_nums = regular_str_path_querying(
        graph, regex, start_node_nums, final_node_nums, mode="cpu"
    )

    assert actual_reachable_state_nums == expected_reachable_state_nums


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
@pytest.mark.skipif(
    not sys.platform == "linux",
    reason="pyCuBool is only supported on Linux platform now",
)
def test_querying_gpu(
    graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums
) -> None:
    actual_reachable_state_nums = regular_str_path_querying(
        graph, regex, start_node_nums, final_node_nums, mode="gpu"
    )

    assert actual_reachable_state_nums == expected_reachable_state_nums
