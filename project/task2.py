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
    dfa = nfa.to_deterministic()
    return dfa


def graph_to_nfa(
        graph: nx.MultiDiGraph, start_nodes: Set[int] = set(), final_nodes: Set[int] = set()
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if len(start_nodes) == 0:
        start_nodes = graph.nodes
    else:
        start_nodes = []

    if len(final_nodes) == 0:
        final_nodes = graph.nodes
    else:
        final_nodes = []

    states = {}

    for node in graph.nodes:
        # graph.nodes(data=True)[node]["is_start"] = False
        # graph.nodes(data=True)[node]["is_final"] = False
        states[node] = State(node)

    for node in start_nodes:
        # graph.nodes(data=True)[node]["is_start"] = True
        nfa.add_start_state(states[node])

    for node in final_nodes:
        # graph.nodes(data=True)[node]["is_final"] = True
        nfa.add_final_state(states[node])

    # eps_edges = []

    for edge in graph.edges(data=True):
        # if edge[2]["label"] == "eps":
        #     # eps_edges.append(edge)
        #     nfa.add_transition(states[edge[0]], Epsilon(), states[edge[1]])
        # else:
        nfa.add_transition(states[edge[0]], Symbol(edge[2]["label"]), states[edge[1]])


    # nfa.remove_epsilon_transitions()

    # for e in eps_edges:
    #     e_to = e[1]
    #     e_from = e[0]
    #     for e2 in graph.edges(data=True):
    #         if e2[0] == e_to:
    #             nfa.add_transition(states[e_from], Epsilon(), states[e2[1]])

    return nfa
