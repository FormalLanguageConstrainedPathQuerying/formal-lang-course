import pytest
from pyformlang.cfg import Variable, Production, Epsilon, Terminal, CFG
from pyformlang.regular_expression import Regex

from project.automaton_tools import get_min_dfa_from_regex, check_regex_equality
from project.grammar_tools import (
    get_cnf_from_file,
    get_wcnf_from_file,
    get_cfg_from_file,
    is_wcnf,
    ECFG,
)


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


@pytest.mark.parametrize(
    "filename, axiom",
    [("epsilon.txt", "E"), ("from_lesson.txt", "S"), ("random.txt", "NP")],
)
def test_wcnf_from_file_start_symbol(filename, axiom):
    path = "tests/data/cfgs/" + filename

    wcnf = get_wcnf_from_file(path, axiom)

    assert wcnf.start_symbol == Variable(axiom)


@pytest.mark.parametrize(
    "filename, axiom, productions",
    [
        ("epsilon.txt", "E", {Production(Variable("E"), [Epsilon()])}),
        (
            "from_lesson.txt",
            "S",
            {
                Production(Variable("b#CNF#"), [Terminal("b")]),
                Production(Variable("C#CNF#1"), [Variable("S"), Variable("b#CNF#")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("S"), [Epsilon()]),
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("S"), [Variable("S"), Variable("S")]),
            },
        ),
        (
            "random.txt",
            "NP",
            {
                Production(Variable("NP"), [Variable("Det"), Variable("CN")]),
                Production(Variable("Det"), [Terminal("the")]),
                Production(Variable("NP"), [Terminal("john")]),
                Production(Variable("CN"), [Variable("CN"), Variable("C#CNF#1")]),
                Production(Variable("CN"), [Terminal("girl")]),
                Production(Variable("S/NP"), [Variable("NP"), Variable("VP/NP")]),
                Production(Variable("VTrans"), [Terminal("loves")]),
                Production(Variable("VP/NP"), [Variable("VTrans"), Variable("NP")]),
                Production(Variable("Wh"), [Terminal("whom")]),
                Production(Variable("C#CNF#1"), [Variable("Wh"), Variable("S/NP")]),
            },
        ),
    ],
)
def test_wcnf_from_file_productions(filename, axiom, productions):
    path = "tests/data/cfgs/" + filename

    wcnf = get_wcnf_from_file(path, axiom)
    print()
    assert set(wcnf.productions) == productions


@pytest.mark.parametrize(
    "filename, axiom",
    [("epsilon.txt", "E"), ("from_lesson.txt", "S"), ("random.txt", "NP")],
)
def test_wcnf_from_file(filename, axiom):
    path = "tests/data/cfgs/" + filename

    wcnf = get_wcnf_from_file(path, axiom)
    cfg = get_cfg_from_file(path, axiom)

    assert is_wcnf(wcnf, cfg)


@pytest.mark.parametrize(
    "cfg, expected_ecfg_productions",
    [
        (
            """
            S -> epsilon
            """,
            {Variable("S"): Regex("epsilon")},
        ),
        (
            """
            S -> a S b S
            S -> epsilon
            """,
            {Variable("S"): Regex("(a S b S) | epsilon")},
        ),
        (
            """
            S -> i f ( C ) t h e n { ST } e l s e { ST }
            C -> t r u e | f a l s e
            ST -> p a s s | S
            """,
            {
                Variable("S"): Regex("i f ( C ) t h e n { ST } e l s e { ST }"),
                Variable("C"): Regex("t r u e | f a l s e"),
                Variable("ST"): Regex("p a s s | S"),
            },
        ),
    ],
)
def test_ecfg_productions(cfg, expected_ecfg_productions):
    ecfg = ECFG.from_cfg(CFG.from_text(cfg))
    actual_ecfg_productions = set(ecfg.productions)

    assert all(
        get_min_dfa_from_regex(production.body).is_equivalent_to(
            get_min_dfa_from_regex(expected_ecfg_productions[production.head])
        )
        for production in actual_ecfg_productions
    ) and len(actual_ecfg_productions) == len(expected_ecfg_productions)


@pytest.mark.parametrize(
    "ecfg_text, expected_ecfg_productions",
    [
        (
            """

            """,
            [],
        ),
        (
            """
            S -> a S b S | epsilon
            """,
            {
                Variable("S"): Regex("a S b S | epsilon"),
            },
        ),
        (
            """
            S -> (a | b)* c
            """,
            {Variable("S"): Regex("(a | b)* c")},
        ),
        (
            """
            S -> (a (S | epsilon) b)*
            A -> a b c
            """,
            {
                Variable("S"): Regex("(a (S | epsilon) b)*"),
                Variable("A"): Regex("a b c"),
            },
        ),
    ],
)
def test_ecfg_from_text(ecfg_text, expected_ecfg_productions):
    ecfg = ECFG.from_text(ecfg_text)
    actual_ecfg_productions = set(ecfg.productions)

    assert len(actual_ecfg_productions) == len(expected_ecfg_productions) and all(
        check_regex_equality(p.body, expected_ecfg_productions[p.head])
        for p in ecfg.productions
    )


@pytest.mark.parametrize(
    "cfg_text",
    [
        """
        S -> B -> C
        """,
        """
        A -> b B -> a
        """,
        """
        S -> a S b S
        A -> B ->
        """,
    ],
)
def test_one_production_per_line(cfg_text):
    with pytest.raises(ValueError):
        ECFG.from_text(cfg_text)


@pytest.mark.parametrize(
    "cfg_text",
    [
        """
        S -> B
        S -> A
        """,
        """
        A -> b
        B -> a
        A -> c
        """,
    ],
)
def test_one_production_per_variable(cfg_text):
    with pytest.raises(ValueError):
        ECFG.from_text(cfg_text)
