from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    EpsilonNFA,
)
from pyformlang.regular_expression import Regex
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    nfa = Regex(regex).to_epsilon_nfa()

    if not isinstance(nfa, EpsilonNFA):
        raise ValueError("Unexpected behavior in convertion regex -> nfa")

    dfa: DeterministicFiniteAutomaton = nfa.to_deterministic()

    if not dfa.is_deterministic():
        raise TypeError("Nfa when converting to dfa is not deterministic")

    dfa_minimal = dfa.minimize()

    if not dfa.is_equivalent_to(dfa_minimal):
        raise ValueError("Dfa after minimize is not equivalent")

    return dfa_minimal


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    pass
