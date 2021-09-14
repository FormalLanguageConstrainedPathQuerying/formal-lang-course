from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex

__all__ = ["regex_to_min_dfa"]


def regex_to_min_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Gets a string representation of regular expression and builds equivalent Deterministic Finite Automaton
    Parameters
    ----------
    regex_str: str
        String representation of regular expression
    Returns
    -------
    DeterministicFiniteAutomaton
        Deterministic Finite Automaton, which is equivalent to given regular expression
    Raises
    ------
    MisformedRegexError
        If there is wrong form of string representation of regular expression
    """

    return Regex(regex_str).to_epsilon_nfa().to_deterministic().minimize()
