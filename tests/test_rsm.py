import os
import tempfile
import pytest
import project  # on import will print something from __init__ file
from project.grammar import ecfg_from_cfg
from project.grammar import cfg_from_file
from project.grammar import cfg_to_weak_cnf
from project.rsm import rsm_from_ecfg


def setup_module(module):
    print("grammar setup module")


def teardown_module(module):
    print("grammar teardown module")


def get_cfg_example_():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.write("\n".join(["S -> $ | A | B a", "A -> a | C", "B -> b", "D -> C"]))
        filename = tmp.name
    return cfg_from_file(filename)


def test_1_rsm_from_ecfg():
    ecfg = ecfg_from_cfg(get_cfg_example_())
    rsm = rsm_from_ecfg(ecfg)

    assert rsm["S"].accepts("A")
    assert rsm["S"].accepts("Ba")
    assert rsm["B"].accepts("b")
    assert not rsm["B"].accepts("a")

    print("test_1_rsm_from_ecfg test asserted")


def test_2_rsm_from_weak_cnf():
    cfg = get_cfg_example_()
    rsm = rsm_from_ecfg(ecfg_from_cfg(cfg_to_weak_cnf(cfg)))
    for nfa in rsm:
        assert not nfa.is_empty()

    assert rsm["S"].accepts("a")
    assert rsm["B"].accepts("b")
    assert not rsm["B"].accepts("a")
    print("test_2_rsm_from_weak_cnf asserted")


def test_3_rsm_minimize():
    cfg = get_cfg_example_()
    rsm = rsm_from_ecfg(ecfg_from_cfg(cfg))
    for nfa in rsm:
        assert not nfa.is_empty()

    assert rsm["S"].accepts("A")
    assert rsm["S"].accepts("Ba")
    assert rsm["B"].accepts("b")
    assert not rsm["B"].accepts("a")
    print("test_3_rsm_minimize asserted")
