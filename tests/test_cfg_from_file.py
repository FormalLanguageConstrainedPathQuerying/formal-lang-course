import pytest

from pyformlang.cfg import Production, Variable, Terminal
from project.cfg_utils import *


@pytest.mark.parametrize(
    "cfg_as_text",
    ["", "A -> b"],
)
def test_empty_cfg_from_file(tmpdir, cfg_as_text):
    file = tmpdir.mkdir("test_dir").join("some_cfg_file")
    file.write(cfg_as_text)
    cfg = cfg_from_file(file)
    assert cfg.is_empty()


@pytest.mark.parametrize(
    "cfg_as_text, expected_productions",
    [
        ("", set()),
        ("S -> a", {Production(Variable("S"), [Terminal("a")])}),
        (
            """
            S -> epsilon
            S -> a S b
            S -> S S
            """,
            {
                Production(Variable("S"), []),
                Production(
                    Variable("S"), [Terminal("a"), Variable("S"), Terminal("b")]
                ),
                Production(Variable("S"), [Variable("S"), Variable("S")]),
            },
        ),
    ],
)
def test_cfg_from_file(tmpdir, cfg_as_text, expected_productions):
    file = tmpdir.mkdir("test_dir").join("some_cfg_file")
    file.write(cfg_as_text)
    cfg = cfg_from_file(file)
    assert cfg.productions == expected_productions
