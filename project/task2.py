from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol
from networkx import MultiDiGraph

from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    regex_obj = Regex(regex)
    nfa = regex_obj.to_epsilon_nfa()
    dfa = nfa.to_deterministic()
    return dfa.minimize()


def graph_to_nfa(
        graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    if start_states is None:
        start_states = set(graph.nodes)
    if final_states is None:
        final_states = set(graph.nodes)

    for state in start_states:
        nfa.add_start_state(State(state))

    for state in final_states:
        nfa.add_final_state(State(state))

    # Добавляем состояния из вершин графа
    # for node in graph.nodes:
    #     nfa.add_state(State(node))

    # Добавляем переходы между состояниями
    for begin, end, data in graph.edges(data=True):
        from_state = State(begin)
        to_state = State(end)
        symbol = Symbol(data["label"])
        nfa.add_transition(from_state, symbol, to_state)

    return nfa
