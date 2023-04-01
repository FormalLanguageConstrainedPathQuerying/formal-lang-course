import tempfile
import pytest
import project  # on import will print something from __init__ file
from project.grammar import cfg_from_file
from project.grammar import cfg_to_weak_cnf
import pyformlang.cfg as pfl_cfg


def setup_module(module):
    print("grammar setup module")


def teardown_module(module):
    print("grammar teardown module")


def test_1_cfg_from_file_empty():
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        tmp.writelines([])
        cfg = cfg_from_file(tmp.name)
        assert cfg.is_empty()

    print("cfg_from_file_empty test asserted")


def test_2_cfg_from_file():
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        tmp.write("\n".join(["S -> A | B a", "A -> a", "B -> b"]))
        tmp.flush()
        cfg = cfg_from_file(tmp.name)
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
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        tmp.write("\n".join(["S -> $ | A | B a", "A -> a | C", "B -> b", "D -> C"]))
        tmp.flush()
        cfg = cfg_from_file(tmp.name)
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
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        tmp.write(
            "\n".join(
                ["F -> A | B a | C", "A -> a | C B | $", "B -> b", "D -> C", "C -> b c"]
            )
        )
        tmp.flush()
        cfg = cfg_from_file(tmp.name, "F")
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
