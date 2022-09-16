from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
)
import networkx as nx


def regex_str_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    return Regex(regex_str).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions([(x, l, y) for x, y, l in graph.edges(data="label") if l])

    nodes = graph.nodes()

    if not start_states:
        start_states = nodes
    elif not start_states.issubset(nodes):
        raise Exception(
            f"Graph does not contain start states: {start_states.difference(set(nodes))}"
        )
    if not final_states:
        final_states = nodes
    elif not final_states.issubset(nodes):
        raise Exception(
            f"Graph does not contain final states: {final_states.difference(set(nodes))}"
        )

    for i in start_states:
        nfa.add_start_state(i)
    for i in final_states:
        nfa.add_final_state(i)

    return nfa.minimize()
