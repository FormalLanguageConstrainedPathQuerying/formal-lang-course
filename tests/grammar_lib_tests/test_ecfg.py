from project.grammar_lib import ecfg_of_file, ecfg_of_cfg, cfg_of_path
from project.extended_context_free_grammar import ECFG
from pyformlang.cfg import Variable, Terminal
from pyformlang.regular_expression import Regex


def compare_ecfg(expected: ECFG, got: ECFG):
    assert expected.variables == got.variables
    assert expected.terminals == got.terminals
    assert expected.starting_symbol == got.starting_symbol

    assert len(expected.productions) == len(got.productions)

    for k in expected.productions.keys():
        assert str(expected.productions[k]) == str(got.productions[k])


def test_ecfg_of_file_1():
    source = "tests/test_grammars/1.ecfg"

    ecfg = ecfg_of_file(source)

    expected = ECFG(
        {Variable("S"), Variable("A"), Variable("B")},
        {Terminal("a"), Terminal("b")},
        {
            Variable("S"): Regex("A | B*"),
            Variable("A"): Regex("a"),
            Variable("B"): Regex("b"),
        },
        Variable("S"),
    )

    compare_ecfg(expected, ecfg)


def test_ecfg_of_file_2():
    source = "tests/test_grammars/2.ecfg"

    ecfg = ecfg_of_file(source)

    expected = ECFG(
        {Variable("S")},
        set(),
        {Variable("S"): Regex("epsilon")},
        Variable("S"),
    )

    compare_ecfg(expected, ecfg)


def test_ecfg_of_file_3():
    source = "tests/test_grammars/3.ecfg"

    ecfg = ecfg_of_file(source)

    expected = ECFG(
        {Variable("S"), Variable("A"), Variable("B"), Variable("C")},
        {
            Terminal("a"),
            Terminal("b"),
            Terminal("c"),
            Terminal("d"),
            Terminal("e"),
            Terminal("f"),
        },
        {
            Variable("S"): Regex("A | B | C | S S | epsilon"),
            Variable("A"): Regex("a S b"),
            Variable("B"): Regex("c S d"),
            Variable("C"): Regex("e S f"),
        },
        Variable("S"),
    )

    compare_ecfg(expected, ecfg)


def test_ecfg_of_cfg():
    cfg_source = "tests/test_grammars/1.cfg"
    cfg = cfg_of_path(cfg_source)
    ecfg = ecfg_of_cfg(cfg)

    expected = ECFG(
        {Variable("S"), Variable("A"), Variable("B"), Variable("C")},
        {Terminal("a"), Terminal("b"), Terminal("c")},
        {
            Variable("S"): Regex("A B C"),
            Variable("A"): Regex("a"),
            Variable("B"): Regex("b"),
            Variable("C"): Regex("c"),
        },
        Variable("S"),
    )

    compare_ecfg(expected, ecfg)
