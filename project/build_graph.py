from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import State
from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int] = None, final_states: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    # Если стартовые или финальные состояния не указаны, используем все вершины графа
    start_states = start_states if start_states else set(graph.nodes)
    final_states = final_states if final_states else set(graph.nodes)

    for s in start_states:
        nfa.add_start_state(State(s))
    for f in final_states:
        nfa.add_final_state(State(f))

    for u, v, data in graph.edges(data=True):
        label = data.get("label", "")
        nfa.add_transition(State(u), label, State(v))

    return nfa
