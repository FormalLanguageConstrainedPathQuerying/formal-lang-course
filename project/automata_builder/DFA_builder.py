from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def build_mdfa(input: str) -> DeterministicFiniteAutomaton:
    enfa = Regex(input).to_epsilon_nfa()
    if enfa.is_deterministic():
        mdfa = enfa.to_deterministic().minimize()
    else:
        mdfa = enfa.minimize()
    return mdfa
