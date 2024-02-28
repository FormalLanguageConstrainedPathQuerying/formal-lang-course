from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from typing import Set

def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """Return minimized DFA from regular expression string

    Keyword arguments:
    expr -- academic regular expression string;
    """
    dfa = Regex(regex).to_epsilon_nfa()
    return dfa.minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    """Return nondeterministic finite automaton from `networkx.MultiDiGraph` graph

    Keyword arguments:
    graph -- source graph;
    start_states -- set of nodes marked as start states;
    final_states -- set of nodes marked as final states;
    """
    nfa = NondeterministicFiniteAutomaton()

    for node in graph.nodes():
        if node in start_states:
            nfa.add_start_state(node)
        if node in final_states:
            nfa.add_final_state(node)

    for source, dest, label in graph.edges(data="label", default=None):
        if label is not None:
            nfa.add_transition(source, label, dest)

    return nfa