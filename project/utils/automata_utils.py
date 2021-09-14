from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex, MisformedRegexError


class AutomataException(Exception):
    """
    Base exception for automata utils
    """

    def __init__(self, msg):
        self.msg = msg


def transform_regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Transform regular expression into DFA

    Parameters
    ----------
    regex_str: str
        Regular expression represented as string
        https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        Minimal DFA built on given regular expression
    """

    try:
        regex = Regex(regex_str)
    except MisformedRegexError as e:
        raise AutomataException(f"Invalid regular expression")

    enfa = regex.to_epsilon_nfa()

    return enfa.minimize()
