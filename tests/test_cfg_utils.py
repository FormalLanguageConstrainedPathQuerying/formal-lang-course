from pyformlang.cfg import CFG, Terminal, Production
from project.utils import cfg_utils


def test_read_empty_cfg():
    empty = cfg_utils.read_cfg("resources/empty.txt")

    assert empty.is_empty()


def test_read_cfg():
    cfg = cfg_utils.read_cfg("resources/cfg_for_read.txt", "A")

    assert cfg.start_symbol == "A"
    assert cfg.productions == {
        Production(head, body)
        for head, body in [
            ("A", [Terminal("a"), "A"]),
            ("A", [Terminal("b")]),
            ("A", ["B", "C", "D"]),
            ("A", []),
            ("B", ["E"]),
            ("E", ["F"]),
            ("C", ["F", Terminal("c")]),
            ("D", ["A"]),
            ("D", []),
            ("F", [Terminal("t")]),
            ("N", "A"),
        ]
    }


def test_already_in_cnf():
    cnf = cfg_utils.read_cfg("resources/cfg_cnf.txt")
    cnf_transformed = cfg_utils.cfg_to_wcnf(cnf)

    assert cnf.start_symbol == cnf_transformed.start_symbol
    assert cnf.productions == cnf_transformed.productions


def test_already_in_wcnf():
    wcnf = cfg_utils.read_cfg("resources/cfg_wcnf.txt")
    wcnf_transformed = cfg_utils.cfg_to_wcnf(wcnf)

    assert wcnf.start_symbol == wcnf_transformed.start_symbol
    assert wcnf.productions == wcnf_transformed.productions


def test_cfg_to_wcnf():
    cfg = CFG.from_text("S -> a S b S | $")
    wcnf = cfg_utils.cfg_to_wcnf(cfg)

    assert wcnf.start_symbol == "S"
    assert wcnf.productions == {
        Production(head, body)
        for head, body in [
            ("S", []),
            ("S", ["a#CNF#", "C#CNF#1"]),
            ("C#CNF#1", ["S", "C#CNF#2"]),
            ("C#CNF#2", ["b#CNF#", "S"]),
            ("a#CNF#", [Terminal("a")]),
            ("b#CNF#", [Terminal("b")]),
        ]
    }
