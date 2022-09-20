import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex

from project.automata_utils import from_regex_to_dfa

from tests.test_utils import create_automata

testdata = [
    (
        from_regex_to_dfa(Regex("ab")),
        create_automata(
            transitions=[(0, "ab", 1)],
            start_states=[0],
            final_states=[1],
            automata=DeterministicFiniteAutomaton(),
        ),
    ),
    (
        from_regex_to_dfa(Regex("(ab)*")),
        create_automata(
            transitions=[(0, "ab", 0)],
            start_states=[0],
            final_states=[0],
            automata=DeterministicFiniteAutomaton(),
        ),
    ),
    (
        from_regex_to_dfa(Regex("accept|f(ab)*")),
        create_automata(
            transitions=[(0, "accept", 1), (0, "f", 2), (2, "ab", 2)],
            start_states=[0],
            final_states=[1, 2],
            automata=DeterministicFiniteAutomaton(),
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_from_regex_to_dfa(
    actual: DeterministicFiniteAutomaton, expected: DeterministicFiniteAutomaton
):
    assert actual.is_equivalent_to(expected)
