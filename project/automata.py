from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: set[int], final_states: set[int]
) -> NondeterministicFiniteAutomaton:

    states = set(graph.nodes)
    start = states if start_states is None or len(start_states) == 0 else start_states
    final = states if final_states is None or len(final_states) == 0 else final_states

    nfa = NondeterministicFiniteAutomaton()
    for state in start:
        nfa.add_start_state(State(state))
    for state in final:
        nfa.add_final_state(State(state))

    transitions = graph.edges(data=True)
    for u, v, data in transitions:
        nfa.add_transition(State(u), Symbol(data["label"]), State(v))

    return nfa
