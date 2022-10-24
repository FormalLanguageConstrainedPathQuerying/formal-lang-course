from project.__init__ import *

from project.cfg_utils import *


def test_cfg1():
    cfg = (
        read_cfg_from_text(str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg1")
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cfg_wcnf = to_wcnf(cfg)
    cfg_wcnf_exp = read_cfg_from_text(
        str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg1_wcnf"
    )
    assert cfg_wcnf.productions == cfg_wcnf_exp.productions


def test_cfg2():
    cfg = (
        read_cfg_from_text(str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg2")
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cfg_wcnf = to_wcnf(cfg)
    cfg_wcnf_exp = read_cfg_from_text(
        str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg2_wcnf"
    )
    assert cfg_wcnf.productions == cfg_wcnf_exp.productions


def test_cfg3():
    cfg = (
        read_cfg_from_text(
            str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg3_wcnf"
        )
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cfg_wcnf = to_wcnf(cfg)
    cfg_wcnf_exp = read_cfg_from_text(
        str(shared.ROOT) + os.sep + "cfg_files" + os.sep + "cfg3_wcnf"
    )
    assert cfg_wcnf.productions == cfg_wcnf_exp.productions
