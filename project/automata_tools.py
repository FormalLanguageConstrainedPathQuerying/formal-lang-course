from typing import Set
from typing import Optional
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    Epsilon,
    Symbol,
)
from pyformlang.regular_expression import Regex


def regex_to_minimal_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    epsilon_nfa = regex.to_epsilon_nfa()
    dfa_minimal = epsilon_nfa.minimize()
    return dfa_minimal


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Optional[Set], final_states: Optional[Set]
) -> EpsilonNFA:
    epsilon_nfa = EpsilonNFA()

    for src_node, dst_node, data in graph.edges(data=True, default=Epsilon):
        epsilon_nfa.add_transition(
            s_from=src_node, symb_by=Symbol(data["label"]), s_to=dst_node
        )

    all_graph_nodes = set(graph.nodes)

    if start_states is None:
        start_states = all_graph_nodes

    for node in start_states:
        epsilon_nfa.add_start_state(node)

    if final_states is None:
        final_states = all_graph_nodes

    for node in final_states:
        epsilon_nfa.add_final_state(node)

    return epsilon_nfa
