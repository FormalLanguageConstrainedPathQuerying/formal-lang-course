from typing import Set
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
)


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    expr: Regex = Regex(regex)
    nfa: EpsilonNFA = expr.to_epsilon_nfa()
    dfa: DeterministicFiniteAutomaton = nfa.to_deterministic()

    return dfa.minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nodes = [int(node) for node in graph.nodes]

    e_nfa: EpsilonNFA = EpsilonNFA.from_networkx(graph)
    nfa: NondeterministicFiniteAutomaton = e_nfa.remove_epsilon_transitions()

    if not start_states:
        for x in nodes:
            nfa.add_start_state(State(x))
    else:
        for x in start_states:
            nfa.add_start_state(State(x))

    if not final_states:
        for x in nodes:
            nfa.add_final_state(State(x))
    else:
        for x in final_states:
            nfa.add_final_state(State(x))

    return nfa
