from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Epsilon
from pyformlang.finite_automaton import Symbol
import networkx as nx
from typing import Set
import copy


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton or None:
    try:
        regex = Regex(regex)
    except:
        print("Invalid regex format")
        return None

    nfa = regex.to_epsilon_nfa()
    dfa = nfa.to_deterministic().minimize()
    return dfa


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_nodes: Set[int] = set(), final_nodes: Set[int] = set()
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if len(start_nodes) == 0:
        start_nodes = set(graph.nodes)

    if len(final_nodes) == 0:
        final_nodes = set(graph.nodes)

    states = {}

    for node in graph.nodes:
        states[node] = State(node)

    for node in start_nodes:
        nfa.add_start_state(states[node])

    for node in final_nodes:
        nfa.add_final_state(states[node])

    for edge in graph.edges.data(True):
        nfa.add_transition(states[edge[0]], Symbol(edge[2]["label"]), states[edge[1]])

    return nfa
