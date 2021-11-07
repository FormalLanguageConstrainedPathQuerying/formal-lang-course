from project.grammars.cfg_exception import CFGException
from project.utils import CFG_utils
from pyformlang.cfg import CFG, Production, Variable, Terminal

import pytest


def check_epsilons(reachable_symbols, productions_old, productions_nf):
    """
    Test whether all epsilons in reachable variables from initial grammar are present in given normal form
    """
    productions_old_with_epsilon = set(
        filter(
            lambda prod: prod.head in reachable_symbols and not prod.body,
            productions_old,
        )
    )
    productions_nf_with_epsilon = set(
        filter(lambda prod: not prod.body, productions_nf)
    )
    for production in productions_old_with_epsilon:
        if production not in productions_nf_with_epsilon:
            return False
    return True


def is_in_wncf(cfg_nf, cfg_old):
    """
    Test whether given cfg_nf is in Weakened Chomsky NF
    The rules are:
    1. A -> BC, where A, B, C in Variables
    2. A -> a, where A in Variables, a in Terminals
    3. A -> epsilon, where A in Variables
    It is also checked whether every reachable epsilon production from original grammar is present in WNCF
    """
    for production in cfg_nf.productions:
        body = production.body
        if not (
            (len(body) <= 2 and all(map(lambda x: x in cfg_nf.variables, body)))
            or (len(body) == 1 and body[0] in cfg_nf.terminals)
            or (not body)
        ) or not check_epsilons(
            cfg_nf.variables, cfg_old.productions, cfg_nf.productions
        ):
            return False
    return True


@pytest.fixture
def cfg_default():
    variables = {Variable("S"), Variable("B")}
    terminals = {Terminal("1"), Terminal("0")}
    start_symbol = Variable("S")
    productions = {
        Production(Variable("S"), [Terminal("1"), Terminal("0")]),
        Production(Variable("S"), [Terminal("1"), Variable("S"), Terminal("1")]),
        Production(Variable("S"), [Variable("B"), Terminal("1")]),
        Production(Variable("B"), [Terminal("1"), Terminal("1")]),
        Production(Variable("B"), [Variable("S"), Terminal("1")]),
    }
    return CFG(variables, terminals, start_symbol, productions)


@pytest.fixture
def cfg_epsilon():
    grammar = CFG.from_text(
        "S -> a S b S\n\
         S -> epsilon"
    )
    return grammar


@pytest.fixture
def default_normal_form():
    variables = {
        Variable("0#CNF#"),
        Variable("S"),
        Variable("C#CNF#1"),
        Variable("1#CNF#"),
        Variable("B"),
    }
    terminals = {Terminal("0"), Terminal("1")}
    productions = {
        Production(Variable("S"), [Variable("1#CNF#"), Variable("0#CNF#")]),
        Production(Variable("S"), [Variable("B"), Variable("1#CNF#")]),
        Production(Variable("S"), [Variable("1#CNF#"), Variable("C#CNF#1")]),
        Production(Variable("B"), [Variable("S"), Variable("1#CNF#")]),
        Production(Variable("B"), [Variable("1#CNF#"), Variable("1#CNF#")]),
        Production(Variable("0#CNF#"), [Terminal("0")]),
        Production(Variable("1#CNF#"), [Terminal("1")]),
        Production(Variable("C#CNF#1"), [Variable("S"), Variable("1#CNF#")]),
    }
    start_symbol = Variable("S")
    return CFG(variables, terminals, start_symbol, productions)


@pytest.mark.parametrize(
    "cfg_string,start_state",
    [
        (
            "S -> a S b S\n\
         S -> epsilon",
            "S",
        ),
        (
            "S -> A B\n\
         A -> a B c B\n\
         B -> d e f",
            "S",
        ),
        (
            "Expr -> Term | Expr AddOp Term | AddOp Term\n\
          Term -> Factor | Term MulOp Factor\n\
          Factor -> Primary | Factor pow Primary\n\
          Primary -> number | variable\n\
          AddOp -> add | sub\n\
          MulOp -> mul | div",
            "Expr",
        ),
        (
            "S -> A | epsilon\n\
          A -> a b | epsilon\n\
          B -> epsilon",
            "S",
        ),
        (
            "S -> A e | a b\n\
          A -> f g | epsilon\n\
          B -> C | c d",
            "S",
        ),
        ("S -> epsilon", "S"),
    ],
)
def test_is_wncf(cfg_string, start_state):
    cfg = CFG.from_text(cfg_string, start_state)
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg)
    assert is_in_wncf(cfg_in_wncf, cfg)


def test_cfg_to_wncf_productions(cfg_default, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg_default)
    assert cfg_in_wncf.productions == default_normal_form.productions


def test_cfg_to_wncf_start_symbol(cfg_default, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg_default)
    assert cfg_in_wncf.start_symbol == default_normal_form.start_symbol


def test_cfg_from_file(cfg_default):
    filename = "tests/data/test_cfg.txt"
    cfg = CFG_utils.read_cfg_from_file(filename, "S")
    assert cfg.productions == cfg_default.productions


def test_corrupted_cfg():
    with pytest.raises(CFGException):
        filename = "tests/data/test_cfg_corrupted.txt"
        CFG_utils.read_cfg_from_file(filename, "S")


def test_nonexistent_file():
    with pytest.raises(CFGException):
        filename = "Whiteboards are remarkable"
        CFG_utils.read_cfg_from_file(filename, "S")
