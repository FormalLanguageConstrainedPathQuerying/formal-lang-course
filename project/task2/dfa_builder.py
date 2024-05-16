from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex, MisformedRegexError


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """
    Generate minimal deterministic finite automaton by regular expression
    :param regex: regular expression that automata would recognize
    :return: Genereted automata
    """
    try:
        r = Regex(regex)
        return r.to_epsilon_nfa().minimize()
    except MisformedRegexError:
        raise ValueError(f"Invalid regular expression: {regex}")
