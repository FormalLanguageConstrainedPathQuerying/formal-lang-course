from project.grammar_lib import wcnf_of_cfg, cfg_of_path
from pyformlang.cfg import Epsilon


def check_wcnf(cfg):
    for produnction in cfg.productions:
        body = produnction.body
        # A -> a
        if len(body) == 1 and body[0] in cfg.terminals:
            continue

        # A -> B C
        if len(body) == 2 and body[0] in cfg.variables and body[1] in cfg.variables:
            continue

        # A -> eps
        if len(body) == 0:
            continue

        return False
    return True


def test_wcnf_of_cfg_1():
    cfg = cfg_of_path("tests/test_grammars/1.cfg")
    wcnf = wcnf_of_cfg(cfg)

    assert check_wcnf(wcnf)


def test_wcnf_of_cfg_2():
    cfg = cfg_of_path("tests/test_grammars/2.cfg")
    wcnf = wcnf_of_cfg(cfg)

    assert check_wcnf(wcnf)


def test_wcnf_of_cfg_3():
    cfg = cfg_of_path("tests/test_grammars/3.cfg")
    wcnf = wcnf_of_cfg(cfg)

    assert check_wcnf(wcnf)


def test_wcnf_of_cfg_4():
    cfg = cfg_of_path("tests/test_grammars/4.cfg")
    wcnf = wcnf_of_cfg(cfg)

    assert check_wcnf(wcnf)


def test_wcnf_of_cfg_5():
    cfg = cfg_of_path("tests/test_grammars/5.cfg")
    wcnf = wcnf_of_cfg(cfg)

    assert check_wcnf(wcnf)
