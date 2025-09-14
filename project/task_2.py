from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    dfa = Regex(regex).to_epsilon_nfa().to_deterministic().minimize()

    return dfa

def graph_to_nfa(
    graph: MultiDiGraph,
    start_states: set[int],
    final_states: set[int]) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    start_nodes = start_states if start_states else set(graph.nodes)
    for state in start_nodes:
        nfa.add_start_state(State(state))

    final_nodes = final_states if final_states else set(graph.nodes)
    for state in final_nodes:
        nfa.add_final_state(State(state))

    return nfa
