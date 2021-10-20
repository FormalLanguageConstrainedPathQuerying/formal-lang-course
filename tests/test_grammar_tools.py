import pytest
from pyformlang.cfg import Variable, Production, Epsilon, Terminal

from project.grammar_tools import get_cnf_from_file


def test_wrong_file():
    path_not_exists = "tests/data/cfgs/emp"
    path_not_txt = "tests/data/cfgs/empty"
    path_to_empty = "tests/data/cfgs/empty.txt"

    with pytest.raises(OSError):
        get_cnf_from_file(path_not_exists)
    with pytest.raises(OSError):
        get_cnf_from_file(path_not_txt)
    with pytest.raises(OSError):
        get_cnf_from_file(path_to_empty)


def test_wrong_text():
    with pytest.raises(ValueError):
        get_cnf_from_file("tests/data/cfgs/wrong.txt")


@pytest.mark.parametrize(
    "filename, axiom",
    [("epsilon.txt", "E"), ("from_lesson.txt", "S"), ("random.txt", "NP")],
)
def test_cnf_from_file_start_symbol(filename, axiom):
    path = "tests/data/cfgs/" + filename

    c_cnf, _ = get_cnf_from_file(path, axiom)

    assert c_cnf.start_symbol == Variable(axiom)


@pytest.mark.parametrize(
    "filename, axiom, productions",
    [
        ("epsilon.txt", "E", {Production(Variable("E"), [Epsilon()])}),
        (
            "from_lesson.txt",
            "S",
            {
                Production(Variable("S"), [Variable("S"), Variable("S")]),
                Production(Variable("b#CNF#"), [Terminal("b")]),
                Production(Variable("S"), [Epsilon()]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("b#CNF#")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("C#CNF#1"), [Variable("S"), Variable("b#CNF#")]),
                Production(Variable("a#CNF#"), [Terminal("a")]),
            },
        ),
        (
            "random.txt",
            "NP",
            {
                Production(Variable("CN"), [Terminal("girl")]),
                Production(Variable("Det"), [Terminal("the")]),
                Production(Variable("Wh"), [Terminal("whom")]),
                Production(Variable("S/NP"), [Variable("NP"), Variable("VP/NP")]),
                Production(Variable("VTrans"), [Terminal("loves")]),
                Production(Variable("NP"), [Variable("Det"), Variable("CN")]),
                Production(Variable("VP/NP"), [Variable("VTrans"), Variable("NP")]),
                Production(Variable("NP"), [Terminal("john")]),
                Production(Variable("C#CNF#1"), [Variable("Wh"), Variable("S/NP")]),
                Production(Variable("CN"), [Variable("CN"), Variable("C#CNF#1")]),
            },
        ),
    ],
)
def test_cnf_from_file_productions(filename, axiom, productions):
    path = "tests/data/cfgs/" + filename

    c_cnf, _ = get_cnf_from_file(path, axiom)

    assert set(c_cnf.productions) == productions


@pytest.mark.parametrize(
    "filename, axiom",
    [("epsilon.txt", "E"), ("from_lesson.txt", "S"), ("random.txt", "NP")],
)
def test_cnf_from_file(filename, axiom):
    path = "tests/data/cfgs/" + filename

    _, h_cnf = get_cnf_from_file(path, axiom)

    # It means Weak Chomsky Normal Form too
    assert h_cnf.is_normal_form()
