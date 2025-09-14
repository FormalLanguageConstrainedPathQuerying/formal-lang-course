from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_dfa().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    # Definition of the NFA

    nfa = NondeterministicFiniteAutomaton()
    states = [State(i) for i in range(len(graph))]
    for ss in start_states:
        nfa.add_start_state(ss)
    for fs in final_states:
        nfa.add_final_state(fs)
    symbs = dict()
    for u, v, label in graph.edges(data="label"):
        symb = symbs[label]
        if symb is None:
            symb = Symbol(label)
            symbs[label] = symb
        nfa.add_transition(states[u], symb, states[v])

    return nfa
