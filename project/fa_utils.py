from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from networkx import MultiDiGraph


def regex2dfa(regex: str) -> DeterministicFiniteAutomaton:
    """
    Builds a minimal DFA for a given regular expression

    Args:
        regex: regular expression

    Returns:
        Minimal DFA
    """
    return Regex(regex).to_epsilon_nfa().minimize()


def graph2nfa(
    graph: MultiDiGraph, start_states: [int] = None, final_states: [int] = None
) -> NondeterministicFiniteAutomaton:
    """
    Builds a NFA for given graph

    Args:
        graph: the graph on which the automaton will be built
        start_states: numbers of vertices corresponding to the initial states of the automaton
        final_state: numbers of vertices corresponding to the final states of the automaton

    Returns:
        NFA for a given graph
    """

    fa = NondeterministicFiniteAutomaton()

    if start_states is None:
        start_states = graph.nodes
    list(map(fa.add_start_state, start_states))

    if final_states is None:
        final_states = graph.nodes
    list(map(fa.add_final_state, final_states))

    for source, dest, label in graph.edges(data="label"):
        fa.add_transition(source, label, dest)

    return fa
