from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
from typing import Set


# function for constructing a minimal DFA for a given regular expression
def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    enfa = Regex(regex).to_epsilon_nfa()
    dfa = enfa.remove_epsilon_transitions().to_deterministic().minimize()

    return dfa


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    all_states = set(int(node) for node in graph.nodes)

    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    if start_states:
        for i in start_states:
            nfa.add_start_state(State(i))
    else:
        for i in all_states:
            nfa.add_start_state(State(i))

    if final_states:
        for i in final_states:
            nfa.add_final_state(State(i))
    else:
        for i in all_states:
            nfa.add_final_state(State(i))

    return nfa
