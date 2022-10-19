import time
from collections import Counter

import cfpq_data
import pytest
from prettytable import PrettyTable
from pyformlang.regular_expression import PythonRegex, Regex
from scipy import stats, mean
from scipy.sparse import csr_matrix, dok_matrix, csc_matrix

from project.rpq import *


@pytest.mark.parametrize(
    "regex,start_states,final_states,expected",
    [
        ("a*b*", {1}, {6}, {(1, 6)}),
        ("aa", {0}, {2}, {(0, 2)}),
        ("(a|c)*b", {0, 1}, {4, 5}, {(0, 4), (1, 4)}),
        ("d*a*n*i*e*l*", {0}, {1, 2, 3}, {(0, 1), (0, 2), (0, 3)}),
    ],
)
@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_rpq(two_cycles_graph, regex, start_states, final_states, expected):
    request = PythonRegex(regex)
    ans = rpq_by_tensor(two_cycles_graph, request, start_states, final_states)
    assert ans == expected


@pytest.mark.parametrize(
    "regex,start_states,final_states,expected",
    [
        ("a*b*", {1}, {6}, {6}),
        ("aa", {0}, {2}, {2}),
        ("(a|c)*b", {0, 1}, {4, 5}, {4}),
        ("d*a*n*i*e*l*", {0, 1}, {1, 2, 3}, {1, 2, 3}),
    ],
)
@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_rpq_by_bfs(two_cycles_graph, regex, start_states, final_states, expected):
    request = PythonRegex(regex)
    ans = rpq_by_bfs(two_cycles_graph, request, start_states, final_states, False)
    assert ans == expected


@pytest.mark.parametrize(
    "regex,start_states,final_states,expected",
    [
        ("a*b*", {1}, {6}, {(1, 6)}),
        ("aa", {0}, {2}, {(0, 2)}),
        ("(a|c)*b", {0, 1}, {4, 5}, {(0, 4), (1, 4)}),
        (
            "d*a*n*i*e*l*",
            {0, 1},
            {1, 2, 3},
            {(0, 1), (1, 2), (1, 1), (0, 3), (0, 2), (1, 3)},
        ),
    ],
)
@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_rpq_by_bfs_for_each_start(
    two_cycles_graph, regex, start_states, final_states, expected
):
    request = PythonRegex(regex)
    ans = rpq_by_bfs(two_cycles_graph, request, start_states, final_states, True)
    assert ans == expected
