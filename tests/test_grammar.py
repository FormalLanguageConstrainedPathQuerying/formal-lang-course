import os
import tempfile
import pytest
import project  # on import will print something from __init__ file
from project.grammar import ecfg_from_cfg
from project.grammar import cfg_from_file
from project.grammar import cfg_to_weak_cnf
import pyformlang.cfg as pfl_cfg


def setup_module(module):
    print("grammar setup module")


def teardown_module(module):
    print("grammar teardown module")


def test_1_cfg_from_file_empty():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.writelines([])
        filename = tmp.name
    cfg = cfg_from_file(filename)
    assert cfg.is_empty()

    print("cfg_from_file_empty test asserted")


def test_2_cfg_from_file():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.write("\n".join(["S -> A | B a", "A -> a", "B -> b"]))
        filename = tmp.name
    cfg = cfg_from_file(filename)
    assert not cfg.is_empty()
    assert len(cfg.productions) == 4
    assert (
        pfl_cfg.Production(pfl_cfg.Variable("A"), [pfl_cfg.Terminal("a")])
        in cfg.productions
    )
    assert (
        pfl_cfg.Production(pfl_cfg.Variable("S"), [pfl_cfg.Variable("A")])
        in cfg.productions
    )
    assert (
        pfl_cfg.Production(
            pfl_cfg.Variable("S"), [pfl_cfg.Variable("B"), pfl_cfg.Terminal("a")]
        )
        in cfg.productions
    )
    assert (
        pfl_cfg.Production(pfl_cfg.Variable("S"), [pfl_cfg.Terminal("b")])
        not in cfg.productions
    )
    print("cfg_from_file test asserted")


def test_3_cfg_to_weak_cnf():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.write("\n".join(["S -> $ | A | B a", "A -> a | C", "B -> b", "D -> C"]))
        filename = tmp.name
    cfg = cfg_from_file(filename)
    weak_cnf = cfg_to_weak_cnf(cfg)
    assert not weak_cnf.is_empty()
    assert weak_cnf.variables == {
        pfl_cfg.Variable("S"),
        pfl_cfg.Variable("B"),
        pfl_cfg.Variable("a#CNF#"),
    }
    assert weak_cnf.contains("")
    assert weak_cnf.contains("a")
    assert weak_cnf.contains("ba")
    print("cfg_to_weak_cnf test asserted")


def test_4_cfg_to_weak_cnf_with_start():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.write(
            "\n".join(
                ["F -> A | B a | C", "A -> a | C B | $", "B -> b", "D -> C", "C -> b c"]
            )
        )
        filename = tmp.name
    cfg = cfg_from_file(filename, "F")
    weak_cnf = cfg_to_weak_cnf(cfg)
    assert not weak_cnf.is_empty()
    assert weak_cnf.variables == {
        pfl_cfg.Variable("F"),
        pfl_cfg.Variable("B"),
        pfl_cfg.Variable("C"),
        pfl_cfg.Variable("a#CNF#"),
        pfl_cfg.Variable("b#CNF#"),
        pfl_cfg.Variable("c#CNF#"),
    }
    assert weak_cnf.contains("")
    assert weak_cnf.contains("a")
    assert weak_cnf.contains("ba")
    assert weak_cnf.contains("bc")
    assert weak_cnf.contains("bcb")
    print("cfg_to_weak_cnf_with_start test asserted")


def test_5_extended_context_free_grammars():
    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(os.path.realpath(__file__)), delete=False
    ) as tmp:
        tmp.write("\n".join(["S -> $ | A | B a", "A -> a | C", "B -> b", "D -> C"]))
        filename = tmp.name
    cfg = cfg_from_file(filename)
    ecfg = ecfg_from_cfg(cfg)

    assert len(ecfg.productions) == 4
    assert ecfg.start.value == "S"
    assert ecfg.terminals == {pfl_cfg.Terminal("a"), pfl_cfg.Terminal("b")}
    assert ecfg.variables == {
        pfl_cfg.Variable("S"),
        pfl_cfg.Variable("B"),
        pfl_cfg.Variable("A"),
        pfl_cfg.Variable("C"),
        pfl_cfg.Variable("D"),
    }

    ecfg.productions[pfl_cfg.Variable("S")].accepts("$")
    ecfg.productions[pfl_cfg.Variable("S")].accepts("A")
    ecfg.productions[pfl_cfg.Variable("S")].accepts("B a")
    print("test_5_extended_context_free_grammars asserted")
