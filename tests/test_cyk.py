import os

from project.cfg_manager import CFGManager
from project.cyk import cyk
from pyformlang.cfg import CFG

path = os.path.dirname(os.path.abspath(__file__)) + "/res"


def test_cyk1():
    file_path = path + "/cfg_1"
    cfg = CFGManager.read_cfg_from_file(file_path)

    actual = cyk(cfg, "ab")
    assert not actual

    actual = cyk(cfg, "")
    assert not actual


def test_cyk2():
    file_path = path + "/cfg_2"
    cfg = CFGManager.read_cfg_from_file(file_path)

    actual = cyk(cfg, "ab")
    assert actual

    actual = cyk(cfg, "")
    assert actual


def test_cyk3():
    cfg = CFG.from_text("S -> a S b S | $")

    actual = cyk(cfg, "ab")
    assert actual

    actual = cyk(cfg, "aabb")
    assert actual

    actual = cyk(cfg, "")
    assert actual
