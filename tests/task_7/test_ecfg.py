from typing import Dict

import pytest
from pyformlang import cfg as c
from pyformlang import regular_expression as re

from project.ecfg import ECFG
from tests.utils import read_data_from_json


@pytest.mark.parametrize(
    "cfg",
    read_data_from_json(
        "test_ecfg", lambda data: c.CFG.from_text(data["cfg"], data["start"])
    ),
)
def test_starting_nonterminal(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)

    if cfg.start_symbol is not None:
        assert ecfg.start == cfg.start_symbol
    else:
        assert ecfg.start == c.Variable("S")


@pytest.mark.parametrize(
    "cfg",
    read_data_from_json(
        "test_ecfg", lambda data: c.CFG.from_text(data["cfg"], data["start"])
    ),
)
def test_nonterminals(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)
    vars = (
        cfg.variables
        if cfg.start_symbol is not None
        else (cfg.variables.union({c.Variable("S")}))
    )

    assert ecfg.variables == vars


@pytest.mark.parametrize(
    "cfg",
    read_data_from_json(
        "test_ecfg", lambda data: c.CFG.from_text(data["cfg"], data["start"])
    ),
)
def test_terminals(cfg: c.CFG):
    ecfg = ECFG.from_cfg(cfg)
    assert ecfg.terminals == cfg.terminals


@pytest.mark.parametrize(
    "cfg, expected",
    read_data_from_json(
        "test_ecfg",
        lambda data: (
            c.CFG.from_text(data["cfg"], data["start"]),
            {
                c.Variable(p["head"]): re.Regex(p["body"])
                for p in data["expected_productions"]
            },
        ),
    ),
)
def test_productions(cfg: c.CFG, expected: Dict[c.Variable, re.Regex]):
    ecfg = ECFG.from_cfg(cfg)

    assert len(ecfg.productions) == len(expected)
    for head in expected:
        actual_nfa = ecfg.productions[head].to_epsilon_nfa()
        expected_nfa = expected[head].to_epsilon_nfa()
        assert actual_nfa.is_equivalent_to(expected_nfa)
