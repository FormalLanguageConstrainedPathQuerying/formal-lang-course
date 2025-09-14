from pyformlang import (
    DeterministicFiniteAutomaton,
    Regex,
    NondeterministicFiniteAutomaton,
)
from networkx import MultiDiGraph
from types import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_dfa().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    pass
