import os

from project.cfg_manager import CFGManager
from project.ecfg_manager import ECFGManager
from project.rsm_manager import RSMManager
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

path = os.path.dirname(os.path.abspath(__file__)) + "/res"


def test_create_rsm_from_ecfg1():
    file_path = path + "/cfg_1"
    cfg = CFGManager.read_cfg_from_file(file_path)
    ecnf = ECFGManager.create_from_cfg(cfg)
    rsm = RSMManager.create_rsm_from_ecfg(ecnf)

    assert rsm.boxes == dict()


def test_create_rsm_from_ecfg2():
    file_path = path + "/cfg_2"
    cfg = CFGManager.read_cfg_from_file(file_path)
    ecnf = ECFGManager.create_from_cfg(cfg)
    rsm = RSMManager.create_rsm_from_ecfg(ecnf)

    assert rsm.start_symbol == Variable("S")
    assert rsm.boxes[Variable("S")] == Regex("a.S.b.S | ").to_epsilon_nfa()
    assert rsm.boxes[Variable("X")] == Regex("x.o").to_epsilon_nfa()
    assert rsm.boxes[Variable("T")] == Regex("z.X.c").to_epsilon_nfa()
