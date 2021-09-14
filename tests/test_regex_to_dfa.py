from project.utils import automata_utils
from pyformlang.finite_automaton import Symbol, State

import pytest


def test_is_deterministic():
    dfa = automata_utils.transform_regex_to_dfa("1*00*.1")

    assert dfa.is_deterministic()


def test_is_minimal():
    dfa = automata_utils.transform_regex_to_dfa("1* 0 0")
    dfa_minimal = dfa.minimize()

    assert dfa.is_equivalent_to(dfa_minimal)


def test_expected_dfa():
    regex = "1* 0 0"
    dfa = automata_utils.transform_regex_to_dfa(regex)

    expected_dfa = automata_utils.DeterministicFiniteAutomaton()

    expected_dfa.add_transitions(
        [
            (State(0), Symbol("1"), State(0)),
            (State(0), Symbol("0"), State(1)),
            (State(1), Symbol("0"), State(2)),
        ]
    )

    expected_dfa.add_start_state(State(0))
    expected_dfa.add_final_state(State(2))

    assert dfa.is_equivalent_to(expected_dfa)


def test_incorrect_regex():
    with pytest.raises(automata_utils.AutomataException):
        regex = "++++"
        automata_utils.transform_regex_to_dfa(regex)


@pytest.mark.parametrize(
    "regex_str,word",
    [
        ("1* 0 0", [Symbol("1"), Symbol("1"), Symbol("0"), Symbol("0")]),
        ("abc|d", [Symbol("abc")]),
        ("a abc", [Symbol("a"), Symbol("abc")]),
        ("0 *", [Symbol("0"), Symbol("0")]),
        ("0 *", [Symbol("0")]),
        ("0 *", []),
    ],
)
def test_are_equal_regex_dfa(regex_str, word):
    dfa = automata_utils.transform_regex_to_dfa(regex_str)

    assert dfa.accepts(word)


def test_empty_regex_dfa():
    empty_regex = ""
    dfa = automata_utils.transform_regex_to_dfa(empty_regex)

    assert dfa.is_empty()
