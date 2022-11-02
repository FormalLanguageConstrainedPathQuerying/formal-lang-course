import os

from pyformlang.cfg import Variable
from project.cfg_manager import CFGManager
from project.ecfg_manager import ECFGManager
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol

path = os.path.dirname(os.path.abspath(__file__)) + "/res"


def test_create_from_cfg1():
    file_path = path + "/cfg_1"
    cfg = CFGManager.read_cfg_from_file(file_path)
    ecnf = ECFGManager.create_from_cfg(cfg)

    assert ecnf.productions == dict()


def test_create_from_cfg2():
    file_path = path + "/cfg_2"
    cfg = CFGManager.read_cfg_from_file(file_path)
    ecnf = ECFGManager.create_from_cfg(cfg)

    assert ecnf.start_symbol == Variable("S")
    assert list(map(lambda x: x.head.value, ecnf.productions[Variable("X")].sons)) == [
        Symbol("x"),
        Symbol("o"),
    ]
