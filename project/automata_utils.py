from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["from_regex_to_dfa"]


def from_regex_to_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Converts regex to DFA

    :param regex: regex to be converted
    :return: DeterministicFiniteAutomaton object representing given regex
    """
    return regex.to_epsilon_nfa().to_deterministic().minimize()
