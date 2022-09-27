from project import reg_str_to_dfa
from test_graphs import all_test_graphs, acception_test
import pytest
from pyformlang.regular_expression import MisformedRegexError


def test_regex_str_to_dfa_wrong():
    with pytest.raises(MisformedRegexError):
        reg_str_to_dfa("[*|.]")


def test_regex_str_to_dfa():
    for graph in all_test_graphs:
        dfa = reg_str_to_dfa(graph.reg)
        acception_test(dfa, graph)
