from project import *
from tests.test_graphs import *
import pytest
from pyformlang.regular_expression import MisformedRegexError


def test_regex_str_to_dfa_wrong():
    with pytest.raises(MisformedRegexError):
        regex_str_to_dfa("[*|.]")


def test_regex_str_to_dfa():
    for graph in all_test_graphs:
        dfa = regex_str_to_dfa(graph.reg)
        for accept in graph.accepts:
            assert dfa.accepts(accept), f'{graph.name} failed, "{accept}" not accepted'
        for reject in graph.rejects:
            assert not dfa.accepts(
                reject
            ), f'{graph.name} failed, "{reject}" not rejected'
