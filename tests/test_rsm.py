import pytest
from pyformlang.cfg import Variable
import project  # on import will print something from __init__ file
from project.grammar import ECFG
from project.rsm import rsm_from_ecfg


def setup_module(module):
    print("grammar setup module")


def teardown_module(module):
    print("grammar teardown module")


def get_ecfg_example_():
    return ECFG.from_string("\n".join(["S -> $ | A | B a", "A -> a | a B", "B -> b"]))


def test_1_rsm_from_ecfg():
    rsm = rsm_from_ecfg(get_ecfg_example_())
    assert rsm["S"].accepts("A")
    assert rsm["S"].accepts("Ba")
    assert rsm["B"].accepts("b")
    assert not rsm["B"].accepts("a")
    print("test_1_rsm_from_ecfg test asserted")


def test_2_rsm_minimize():
    rsm = rsm_from_ecfg(get_ecfg_example_()).minimize()
    for nfa in rsm:
        assert not nfa.is_empty()

    assert len(rsm.nfa_dict) == 3
    assert rsm["S"].accepts("A")
    assert rsm["S"].accepts("Ba")
    assert rsm["B"].accepts("b")
    assert not rsm["B"].accepts("a")
    print("test_3_rsm_minimize asserted")
