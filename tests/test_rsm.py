from pyformlang.cfg import Variable
from pyformlang.regular_expression import PythonRegex

from project.__init__ import *
import pytest
from project.ecfg import ECFG
from project.cfg_utils import read_cfg_from_text
from project.rsm import RSM


@pytest.mark.parametrize(
    "path_to_file, prod_exp",
    [
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg1",
            {
                Variable("S"): PythonRegex("A B|D|T"),
                Variable("D"): PythonRegex("Y"),
                Variable("Y"): PythonRegex("z"),
                Variable("A"): PythonRegex("a b"),
                Variable("B"): PythonRegex(""),
            },
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg2",
            {
                Variable("S"): PythonRegex("C D E"),
                Variable("D"): PythonRegex("i"),
                Variable("C"): PythonRegex("f G"),
                Variable("E"): PythonRegex("j"),
                Variable("G"): PythonRegex("h"),
            },
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg3",
            {
                Variable("S"): PythonRegex("A S B|c"),
                Variable("B"): PythonRegex("b"),
                Variable("A"): PythonRegex("a"),
            },
        ),
    ],
)
def test_ecfg_rsm(path_to_file, prod_exp):
    cfg = read_cfg_from_text(path_to_file)
    rsm = RSM.ecfg_to_rsm(ECFG.cfg_to_ecfg(cfg))
    for key in prod_exp.keys():
        dfa_exp = create_min_dfa_by_regex(prod_exp[key])
        assert rsm.boxes[key].is_equivalent_to(dfa_exp)
