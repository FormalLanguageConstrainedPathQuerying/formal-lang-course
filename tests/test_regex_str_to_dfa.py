from project import *
from tests.test_graphs import *
import pytest
from pyformlang.regular_expression import MisformedRegexError


def test_regex_str_to_dfa_wrong():
    with pytest.raises(MisformedRegexError):
        regex_str_to_dfa("[*|.]")


def test_regex_str_to_dfa_power_two():
    dfa = regex_str_to_dfa(power_two().reg)
    assert dfa.is_deterministic
    for i in range(1, 5):
        assert dfa.accepts("{0:b}".format(2**i))
    assert not dfa.accepts("0")
    assert not dfa.accepts("1001")


def test_regex_str_to_dfa_binary_mess_ended_by_zero():
    dfa = regex_str_to_dfa(binary_mess_ended_by_zero().reg)
    assert dfa.is_deterministic
    for i in range(0, 42, 2):
        assert dfa.accepts("{0:b}".format(i))
        assert not dfa.accepts("{0:b}".format(i + 1))
