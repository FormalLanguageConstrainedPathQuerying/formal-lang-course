from project.__init__ import *
import pytest
from project.cfg_utils import *


@pytest.mark.parametrize(
    "path_to_file, path_to_file_wcnf",
    [
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg1",
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg1_wcnf",
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg2",
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg2_wcnf",
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg3",
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg3_wcnf",
        ),
    ],
)
def test_cfg1(path_to_file, path_to_file_wcnf):
    cfg = (
        read_cfg_from_text(path_to_file)
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cfg_wcnf = to_wcnf(cfg)
    cfg_wcnf_exp = read_cfg_from_text(path_to_file_wcnf)
    assert cfg_wcnf.productions == cfg_wcnf_exp.productions
