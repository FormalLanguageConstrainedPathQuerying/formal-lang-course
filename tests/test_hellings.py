from pyformlang.cfg import Variable, CFG
from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex as RG

from project.my_cfg import ECFG
from project.hellings import RA


def test_convert_cfg_to_ecfg():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    ecfg = ECFG.convert_cfg(initial)
    expected_production = {
        Variable("S"): RG("A S B | c"),
        Variable("B"): RG("b"),
        Variable("A"): RG("a"),
    }
    for key in expected_production.keys():
        actual = ecfg.ps[key].to_epsilon_nfa()
        expected = expected_production[key].to_epsilon_nfa()

        if actual.is_empty() and expected.is_empty():
            continue
        assert expected.is_equivalent_to(actual)


def test_convert_ecfg_to_recursive_automath():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    ecfg = ECFG.convert_cfg(initial)
    expected_production = {
        Variable("S"): RG("A S B | c"),
        Variable("B"): RG("b"),
        Variable("A"): RG("a"),
    }
    actual = RA.convert_ecfg(ecfg)
    for key in expected_production.keys():
        expected = expected_production[key].to_epsilon_nfa()
        if expected.is_empty() and actual.boxes[key].is_empty():
            continue
        assert actual.boxes[key].is_equivalent_to(expected)


def test_convert_to_adjacency_matrices():
    recursive = RA.convert_ecfg(ECFG.convert_text("S -> a S b | c"))
    states, matrix = recursive.matrices()
    assert len(matrix[State("S")]) == 1
    assert len(matrix[State("a")]) == 1
    assert len(matrix[State("b")]) == 1
    assert len(matrix[State("c")]) == 1
    assert len(states) == 10
    assert len(matrix) == 5
