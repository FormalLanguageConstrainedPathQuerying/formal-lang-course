import pytest
from pathlib import Path
from pyformlang import cfg as c

from project import cfg
import tests.utils as t


def cfg_eq(x: c.CFG, y: c.CFG):
    return x.start_symbol == y.start_symbol and x.productions == y.productions


@pytest.fixture
def path(request, tmp_path: Path) -> Path:
    cfg = request.param

    path = tmp_path / "cfg.txt"
    with open(path, "w") as f:
        f.write(cfg)
    return path


@pytest.mark.parametrize(
    "path, start, expected",
    t.get_data(
        "test_cfg",
        lambda d: (
            d["cfg"],
            d["start"],
            c.CFG.from_text(
                d["cfg"],
                c.Variable(d["start"]),
            )
            if d["start"] is not None
            else c.CFG.from_text(d["cfg"]),
        ),
    ),
    indirect=["path"],
)
def test_read_cfg(path, start: str, expected: c.CFG):
    actual = cfg.read_cfg(path, start) if start is not None else cfg.read_cfg(path)

    assert cfg_eq(actual, expected)


@pytest.mark.parametrize(
    "raw_cfg, start, expected",
    t.get_data(
        "test_cfg",
        lambda d: (
            d["cfg"],
            d["start"],
            c.CFG.from_text(
                d["wcnf"],
                c.Variable(d["start"]),
            )
            if d["start"] is not None
            else c.CFG.from_text(d["wcnf"]),
        ),
    ),
)
def test_cfg_to_wcnf(raw_cfg: str, start: str, expected: c.CFG):
    actual = (
        cfg.cfg_to_wcnf(raw_cfg, start)
        if start is not None
        else cfg.cfg_to_wcnf(raw_cfg)
    )
    assert cfg_eq(actual, expected)
