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
    nodes = graph.nodes

    # https://pyformlang.readthedocs.io/en/latest/modules/finite_automaton.html#pyformlang.finite_automaton.FiniteAutomaton.from_networkx
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    if start_states:
        nfa.add_start_state(State(i) for i in start_states)
    else:
        nfa.add_start_state(State(i) for i in nodes)

    if final_states:
        nfa.add_final_state(State(i) for i in final_states)
    else:
        nfa.add_final_state(State(i) for i in nodes)

    return nfa
