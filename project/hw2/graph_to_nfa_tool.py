from typing import Set

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    all_states = nfa.states
    if not start_states and not final_states:
        for st in all_states:
            nfa.add_start_state(st)
            nfa.add_final_state(st)

    elif not start_states and final_states:
        for st in final_states:
            nfa.add_final_state(State(st))
        for st in all_states:
            nfa.add_start_state(st)

    elif not final_states and start_states:
        for st in start_states:
            nfa.add_start_state(State(st))
        for st in all_states:
            nfa.add_final_state(st)

    else:
        for st in start_states:
            nfa.add_start_state(State(st))
        for st in final_states:
            nfa.add_final_state(State(st))
    return nfa
