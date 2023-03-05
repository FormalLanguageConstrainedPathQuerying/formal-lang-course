from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from networkx import MultiDiGraph


def regex2dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().minimize()


def graph2nfa(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> NondeterministicFiniteAutomaton:

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
