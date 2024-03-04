from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
import networkx as nx


def regex_to_dfa(exp: str) -> DeterministicFiniteAutomaton:
    return Regex(exp).to_epsilon_nfa().minimize()


def graph_to_nfa(
    graph: nx.MultiDiGraph, starts=[], finals=[]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton(graph)

    if not starts:
        for node in graph.nodes():
            nfa.add_start_state(node)
    if not finals:
        for node in graph.nodes():
            nfa.add_final_state(node)

    for node in starts:
        nfa.add_start_state(node)
    for node in finals:
        nfa.add_final_state(node)
    for a, b, data in graph.edges(data="label"):
        nfa.add_transition(a, data, b)

    return nfa
