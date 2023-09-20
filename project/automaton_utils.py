from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
)
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from project.graph_utils import get_graph_info


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return (
        Regex(regex)
        .to_epsilon_nfa()
        .remove_epsilon_transitions()
        .to_deterministic()
        .minimize()
    )


def graph_to_nfa(
    graph: MultiDiGraph, start_nodes: set = set(), final_nodes: set = set()
) -> NondeterministicFiniteAutomaton:
    nfa = EpsilonNFA.from_networkx(graph).remove_epsilon_transitions()
    if len(start_nodes) == 0:
        start_nodes = get_graph_info(nfa).labels_set
    if len(final_nodes) == 0:
        final_nodes = get_graph_info(nfa).labels_set
    for start_state in start_nodes:
        nfa.add_start_state(State(start_state))
    for final_state in final_nodes:
        nfa.add_final_state(State(final_state))
    return nfa
