import pytest
from pyformlang.cfg import Production, Variable, Terminal, Epsilon
from project.cfg_utils import *


def test_wrong_file_path():
    no_such_path = "tests/test_files/lalala.con"
    empty_file = "tests/data/cfgs/empty.contfrg"

    with pytest.raises(OSError):
        cfg_from_file(no_such_path)
    with pytest.raises(OSError):
        cfg_from_file(empty_file)


@pytest.mark.parametrize(
    "filename, axiom",
    [
        ("test1.contfrg", "N"),
        ("test2.contfrg", "S"),
        ("test3.contfrg", "S"),
        ("test4.contfrg", "NP"),
        ("test5.contfrg", "S"),
    ],
)
def test_start_symbol(filename, axiom):
    path = "tests/test_files/test_cfg_utils/" + filename
    cfg = cfg_from_file(path, axiom)
    assert cfg.start_symbol == Variable(axiom)


@pytest.mark.parametrize(
    "filename, axiom, productions",
    [
        ("test1.contfrg", "N", {Production(Variable("N"), [Epsilon()])}),
        (
            "test2.contfrg",
            "S",
            {
                Production(Variable("S"), []),
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("S")]),
            },
        ),
        (
            "test3.contfrg",
            "S",
            {
                Production(Variable("C#CNF#1"), [Variable("S"), Variable("b#CNF#")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("S"), [Variable("S"), Variable("S")]),
                Production(Variable("b#CNF#"), [Terminal("b")]),
                Production(Variable("S"), []),
                Production(Variable("a#CNF#"), [Terminal("a")]),
            },
        ),
        (
            "test4.contfrg",
            "NP",
            {
                Production(Variable("CN"), [Terminal("boy")]),
                Production(Variable("Det"), [Terminal("the")]),
                Production(Variable("Wh"), [Terminal("whom")]),
                Production(Variable("S/NP"), [Variable("NP"), Variable("VP/NP")]),
                Production(Variable("VTrans"), [Terminal("hates")]),
                Production(Variable("NP"), [Variable("Det"), Variable("CN")]),
                Production(Variable("VP/NP"), [Variable("VTrans"), Variable("NP")]),
                Production(Variable("NP"), [Terminal("mark")]),
                Production(Variable("C#CNF#1"), [Variable("Wh"), Variable("S/NP")]),
                Production(Variable("CN"), [Variable("CN"), Variable("C#CNF#1")]),
            },
        ),
        (
            "test5.contfrg",
            "S",
            {
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("b#CNF#")]),
                Production(Variable("S"), []),
                Production(Variable("b#CNF#"), [Terminal("b")]),
            },
        ),
    ],
)
def test_wcnf_productions(filename, axiom, productions):
    path = "tests/test_files/test_cfg_utils/" + filename
    wcnf = cfg_to_wcnf(cfg_from_file(path, axiom))
    assert set(wcnf.productions) == set(productions)


@pytest.mark.parametrize(
    "filename, axiom",
    [
        ("test1.contfrg", "N"),
        ("test2.contfrg", "S"),
        ("test3.contfrg", "S"),
        ("test4.contfrg", "Expr"),
        ("test5.contfrg", "S"),
    ],
)
def test_get_wcnf_from_file(filename, axiom):
    path = "tests/test_files/test_cfg_utils/" + filename
    cfg_old = cfg_from_file(path, axiom)
    wcnf = cfg_to_wcnf(cfg_old)
    assert is_wcnf(wcnf)
    assert check_epsilon_equivalence(wcnf, cfg_old)
