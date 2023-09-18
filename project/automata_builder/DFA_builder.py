from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def build_mdfa(input: str) -> DeterministicFiniteAutomaton:
    enfa = Regex(input).to_epsilon_nfa()
    mdfa = enfa.to_deterministic().minimize()
    return mdfa
