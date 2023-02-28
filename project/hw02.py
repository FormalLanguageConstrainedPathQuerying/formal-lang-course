from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
import networkx as nx


def make_regex_dfa(expr: str) -> DeterministicFiniteAutomaton:
    regex = Regex(expr)
    nfa = regex.to_epsilon_nfa()
    dfa = nfa.to_deterministic()
    return dfa.minimize()


def make_nfa(g: nx.MultiDiGraph):
    pass
