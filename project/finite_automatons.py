from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
import networkx as nx


def regex_to_dfa(expr: str) -> DeterministicFiniteAutomaton:
    regex = Regex(expr)
    nfa = regex.to_epsilon_nfa()
    dfa = nfa.to_deterministic()
    return dfa.minimize()


def graph_to_nfa(g: nx.MultiDiGraph) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton(g)
    for v, u, data in g.edges(data=True):
        nfa.add_transition(v, data["label"], u)
    return nfa
