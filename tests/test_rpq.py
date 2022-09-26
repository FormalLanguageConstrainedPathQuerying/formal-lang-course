import pytest
from pyformlang.regular_expression import PythonRegex

from project.rpq import *


@pytest.mark.parametrize(
    "regex,start_states,final_states,expected",
    [
        ("a*b*", {1}, {6}, {(1, 6)}),
        ("aa", {0}, {2}, {(0, 2)}),
        ("d*a*n*i*e*l*", {0}, {1, 2, 3}, {(0, 1), (0, 2), (0, 3)}),
    ],
)
@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_rpq(two_cycles_graph, regex, start_states, final_states, expected):
    request = PythonRegex(regex)
    ans = rpq(two_cycles_graph, request, start_states, final_states)
    assert ans == expected
