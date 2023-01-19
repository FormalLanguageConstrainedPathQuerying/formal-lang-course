from typing import Set
from typing import Optional

import networkx as nx
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    Epsilon,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.regular_expression import Regex


def regex_to_minimal_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    epsilon_nfa = regex.to_epsilon_nfa()
    dfa_minimal = epsilon_nfa.minimize()
    return dfa_minimal


def graph_to_nfa(
    graph: nx.Graph,
    start_states: Optional[Set] = None,
    final_states: Optional[Set] = None,
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for node_from, node_to, data in graph.edges(data=True, default=Epsilon):
        nfa.add_transition(State(node_from), Symbol(data["label"]), State(node_to))

    if start_states is None:
        start_states = graph.nodes

    for node in start_states:
        nfa.add_start_state(node)

    if final_states is None:
        final_states = graph.nodes

    for node in final_states:
        nfa.add_final_state(node)

    return nfa


def create_nfa_from_graph(
    graph: nx.Graph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for node_from, node_to, data in graph.edges(data=True):
        nfa.add_transition(
            State(int(node_from)),
            Symbol(data["label"]),
            State(int(node_to)),
        )

    for node in map(lambda node: int(node), graph.nodes):
        if not start_states or node in map(lambda state: int(state), start_states):
            nfa.add_start_state(State(node))
        if not final_states or node in map(lambda state: int(state), final_states):
            nfa.add_final_state(State(node))

    return nfa
