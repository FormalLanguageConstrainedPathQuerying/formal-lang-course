from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol
from networkx import MultiDiGraph

from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    all_nodes = set(graph.nodes())

    for state in start_states or all_nodes:
        nfa.add_start_state(State(state))

    for state in final_states or all_nodes:
        nfa.add_final_state(State(state))

    for begin, end, label in graph.edges.data("label"):
        nfa.add_transition(State(begin), Symbol(label), State(end))

    return nfa
