import os
from project.cfg_manager import CFGManager
from pyformlang.cfg import Terminal, Variable, Production

path = os.path.dirname(os.path.abspath(__file__)) + "/res"


def test_read_cfg_from_file1():
    file_path = path + "/cfg_1"
    cfg = CFGManager.read_cfg_from_file(file_path)

    assert cfg.is_empty()


def test_read_cfg_from_file2():
    file_path = path + "/cfg_2"
    cfg = CFGManager.read_cfg_from_file(file_path)

    assert cfg.terminals == {
        Terminal("a"),
        Terminal("b"),
        Terminal("z"),
        Terminal("x"),
        Terminal("c"),
        Terminal("o"),
    }

    assert cfg.variables == {Variable("S"), Variable("T"), Variable("X")}

    assert cfg.start_symbol == Variable("S")

    assert cfg.productions == {
        Production(Variable("T"), [Terminal("z"), Variable("X"), Terminal("c")]),
        Production(
            Variable("S"), [Terminal("a"), Variable("S"), Terminal("b"), Variable("S")]
        ),
        Production(Variable("S"), []),
        Production(Variable("X"), [Terminal("x"), Terminal("o")]),
    }


def test_convert_cfg_to_wcnf1():
    file_path = path + "/cfg_1"
    cfg = CFGManager.read_cfg_from_file(file_path)
    wcnf = CFGManager.convert_cfg_to_wcnf(cfg)

    assert wcnf.is_empty()


def test_convert_cfg_to_wcnf2():
    file_path = path + "/cfg_2"
    cfg = CFGManager.read_cfg_from_file(file_path)
    wcnf = CFGManager.convert_cfg_to_wcnf(cfg)

    assert wcnf.terminals == {Terminal("a"), Terminal("b")}

    assert wcnf.variables == {
        Variable("S"),
        Variable("b#CNF#"),
        Variable("a#CNF#"),
        Variable("C#CNF#1"),
        Variable("C#CNF#2"),
    }

    assert wcnf.start_symbol == Variable("S")

    assert wcnf.productions == {
        Production(Variable("b#CNF#"), [Terminal("b")]),
        Production(Variable("a#CNF#"), [Terminal("a")]),
        Production(Variable("S"), []),
        Production(Variable("C#CNF#1"), [Variable("S"), Variable("C#CNF#2")]),
        Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
        Production(Variable("C#CNF#2"), [Variable("b#CNF#"), Variable("S")]),
    }
