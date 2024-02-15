from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Epsilon
from pyformlang.finite_automaton import Symbol
import networkx as nx


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
    graph: nx.MultiDiGraph, start_nodes=None, final_nodes=None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if start_nodes is None:
        start_nodes = graph.nodes
    else:
        start_nodes = []

    if final_nodes is None:
        final_nodes = graph.nodes
    else:
        final_nodes = []

    for node in start_nodes:
        nfa.add_start_state(State(node))

    for node in final_nodes:
        nfa.add_final_state(State(node))

    for edge in graph.edges(data=True):
        if edge[2]["label"] == "eps":
            nfa.add_transition(State(edge[0]), Epsilon(), State(edge[1]))
        else:
            nfa.add_transition(State(edge[0]), Symbol(edge[2]["label"]), State(edge[1]))

    return nfa
