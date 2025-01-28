from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    regex_obj = Regex(regex)
    nfa: EpsilonNFA = regex_obj.to_epsilon_nfa()
    if not isinstance(nfa, EpsilonNFA):
        raise Exception("Сan't build a NFA based on your regular expression")
    dfa: DeterministicFiniteAutomaton = nfa.to_deterministic()
    min_dfa = dfa.minimize()
    return min_dfa
