from pathlib import Path

import pytest
from tests.utils import read_data_from_json
from project.cfg import cfg_to_wcnf, read_cfg
from pyformlang.cfg import CFG


def eq(cfg1: CFG, cfg2: CFG):
    return cfg1.productions.__eq__(cfg2.productions) and cfg1.start_symbol.__eq__(
        cfg2.start_symbol
    )


@pytest.mark.parametrize(
    "cfg, starting, expected_wcnf",
    read_data_from_json(
        "test_cfg",
        lambda data: (
            data["cfg"],
            data["starting"],
            CFG.from_text(data["wcnf"])
            if data["starting"] is None
            else CFG.from_text(data["wcnf"], data["starting"]),
        ),
    ),
)
def test_cfg_to_wcnf(cfg: str, starting: str, expected_wcnf: CFG):
    if starting is None:
        actual_wcnf = cfg_to_wcnf(cfg)
    else:
        actual_wcnf = cfg_to_wcnf(cfg, starting)

    assert eq(actual_wcnf, expected_wcnf)


@pytest.fixture
def path(request, tmp_path: Path) -> Path:
    cfg = request.param

    path = tmp_path / "cfg.txt"
    with open(path, "w") as f:
        f.write(cfg)
    return path


@pytest.mark.parametrize(
    "path, starting, expected_cfg",
    read_data_from_json(
        "test_cfg",
        lambda data: (
            data["cfg"],
            data["starting"],
            CFG.from_text(data["cfg"])
            if data["starting"] is None
            else CFG.from_text(data["cfg"], data["starting"]),
        ),
    ),
    indirect=["path"],
)
def test_read_cfg(path, starting: str, expected_cfg: CFG):
    actual = read_cfg(path, starting) if starting is not None else read_cfg(path)

    assert eq(actual, expected_cfg)


@pytest.mark.parametrize(
    "cfg",
    read_data_from_json(
        "test_cfg",
        lambda data: (CFG.from_text(data["cfg"])),
    ),
)
def test_to_normal_form(cfg: CFG):
    cnf = cfg.to_normal_form()
    print(cnf)
