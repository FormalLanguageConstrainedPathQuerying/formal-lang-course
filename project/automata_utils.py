from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["from_regex_to_dfa"]


def from_regex_to_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    return regex.to_epsilon_nfa().to_deterministic().minimize()
