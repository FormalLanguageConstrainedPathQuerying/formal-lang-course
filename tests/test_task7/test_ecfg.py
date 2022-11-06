import pytest
from pyformlang import cfg as c
from pyformlang import regular_expression as re

from project.ecfg import ECFG
from tests.utils import get_data


@pytest.mark.parametrize(
    "cfg", get_data("test_ecfg", lambda d: c.CFG.from_text(d["cfg"], d["start"]))
)
def test_vars(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)
    vars = (
        cfg.variables
        if cfg.start_symbol is not None
        else (cfg.variables | {c.Variable("S")})
    )

    assert ecfg.variables == vars


@pytest.mark.parametrize(
    "cfg", get_data("test_ecfg", lambda d: c.CFG.from_text(d["cfg"], d["start"]))
)
def test_terminals(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)
    assert ecfg.terminals == cfg.terminals


@pytest.mark.parametrize(
    "cfg", get_data("test_ecfg", lambda d: c.CFG.from_text(d["cfg"], d["start"]))
)
def test_starts(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)

    if cfg.start_symbol is not None:
        assert ecfg.start == cfg.start_symbol
    else:
        assert ecfg.start == c.Variable("S")


@pytest.mark.parametrize(
    "cfg, expected",
    get_data(
        "test_ecfg",
        lambda d: (
            c.CFG.from_text(d["cfg"], d["start"]),
            {
                c.Variable(p["head"]): re.Regex(p["body"])
                for p in d["expected_productions"]
            },
        ),
    ),
)
def test_eq_productions(cfg: c.CFG, expected: dict[c.Variable, re.Regex]):
    ecfg = ECFG.from_cfg(cfg)

    assert len(ecfg.productions) == len(expected)
    for head in expected:
        actual_nfa = ecfg.productions[head].to_epsilon_nfa()
        expected_nfa = expected[head].to_epsilon_nfa()
        assert actual_nfa.is_equivalent_to(expected_nfa)
