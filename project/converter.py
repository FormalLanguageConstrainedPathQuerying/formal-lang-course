from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton, State
from networkx import MultiDiGraph
from typing import Set

def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    dfa = Regex("abc|d").to_epsilon_nfa().to_deterministic()
    return dfa.minimize()

def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    all_nodes = set(int(node) for node in graph.nodes)

    if len(start_states) == 0:
        start_states = all_nodes
    if len(final_states) == 0:
        final_states = all_nodes

    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa
