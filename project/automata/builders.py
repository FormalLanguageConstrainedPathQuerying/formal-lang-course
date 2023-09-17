from pyformlang.regular_expression import *
from pyformlang.finite_automaton import *


def build_minimal_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """Transforms the regular expression into a minimal DFA

    Parameters
    ----------
    regex : :class:`~pyformlang.regular_expression.Regex`
        The regular expression

    Returns
    ----------
    dfa :  :class:`~pyformlang.deterministic_finite_automaton\
    .DeterministicFiniteAutomaton`
        The minimal DFA

    """
    eps_nfa = regex.to_epsilon_nfa()
    dfa = eps_nfa.to_deterministic().minimize()
    return dfa
