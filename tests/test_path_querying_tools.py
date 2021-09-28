from itertools import product

import pytest

from project.graph_tools import get_two_cycles
from project.path_querying_tools import regular_path_querying


@pytest.fixture
def graph():
    return get_two_cycles(3, 2)


@pytest.mark.parametrize(
    "regex, start_node_nums, final_node_nums, expected_reachable_state_nums",
    [
        (
            "a*|b",
            None,
            None,
            set(product(range(4), range(4))).union({(0, 4), (4, 5), (5, 0)}),
        ),
        ("a*|b", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("a*|b", {4}, {4, 5}, {(4, 5)}),
        ("a.a", {0, 1, 2, 3}, {0, 1, 2, 3}, {(0, 2), (1, 3), (2, 0), (3, 1)}),
        ("b", {0}, {0, 1, 2, 3}, set()),
        ("b*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_querying(
    graph, regex, start_node_nums, final_node_nums, expected_reachable_state_nums
):
    actual_reachable_state_nums = regular_path_querying(
        graph.graph, regex, start_node_nums, final_node_nums
    )

    assert actual_reachable_state_nums == expected_reachable_state_nums
