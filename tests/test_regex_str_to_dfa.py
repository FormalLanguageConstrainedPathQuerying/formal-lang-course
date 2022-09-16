from project.dfa_utils import *
import pytest
from pyformlang.regular_expression import MisformedRegexError
import networkx as nx

reg_wrong = "[*|.]"
reg_power_two = "1 (0)*"
reg_binary_mess_ended_by_zero = "(0|1)* 0"


def test_regex_str_to_dfa_wrong():
    with pytest.raises(MisformedRegexError):
        regex_str_to_dfa(reg_wrong)


def test_regex_str_to_dfa_power_two():
    dfa = regex_str_to_dfa(reg_power_two)
    assert dfa.is_deterministic
    for i in range(1, 5):
        assert dfa.accepts("{0:b}".format(2**i))
    assert not dfa.accepts("0")
    assert not dfa.accepts("1001")


def test_regex_str_to_dfa_binary_mess_ended_by_zero():
    dfa = regex_str_to_dfa(reg_binary_mess_ended_by_zero)
    assert dfa.is_deterministic
    for i in range(0, 42, 2):
        assert dfa.accepts("{0:b}".format(i))
    assert not dfa.accepts("1")
    assert not dfa.accepts("1001")
