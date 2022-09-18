from pyformlang.finite_automaton import DeterministicFiniteAutomaton, Symbol, State
from pyformlang.regular_expression import Regex

from project.automata import *
from tests.utils import *


def test_empty_regex_dfa_has_no_states():
    regex = Regex("")
    regex_dfa = regex_to_min_dfa(regex)
    assert not regex_dfa.states


def test_or_regex_dfa_is_correct():
    regex = Regex("(a|b)(c|d)")
    regex_dfa = regex_to_min_dfa(regex)

    expected_dfa = DeterministicFiniteAutomaton()
    expected_dfa.add_transitions(
        [
            (0, Symbol("a"), 1),
            (0, Symbol("b"), 1),
            (1, Symbol("c"), 2),
            (1, Symbol("d"), 2),
        ]
    )
    expected_dfa.add_start_state(State(0))
    expected_dfa.add_final_state(State(2))

    assert check_automatons_are_equivalent(regex_dfa, expected_dfa)


def test_kleene_star_regex_dfa_is_correct():
    regex = Regex("(a b)*c")
    regex_dfa = regex_to_min_dfa(regex)

    expected_dfa = DeterministicFiniteAutomaton()
    expected_dfa.add_transitions(
        [
            (0, Symbol("a"), 1),
            (1, Symbol("b"), 0),
            (0, Symbol("c"), 2),
        ]
    )
    expected_dfa.add_start_state(State(0))
    expected_dfa.add_final_state(State(2))

    assert check_automatons_are_equivalent(regex_dfa, expected_dfa)
