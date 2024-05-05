from typing import List, Set
from networkx import MultiDiGraph
import pyformlang.regular_expression as re
import pyformlang.finite_automaton.deterministic_finite_automaton as dfa
import pyformlang.finite_automaton.nondeterministic_finite_automaton as ndfa
from pyformlang.finite_automaton import State


def get_nvertex_nedges_numerate_marks_from_graph(
    graph: MultiDiGraph,
) -> tuple[int, int, List]:
    """
    Получить количество вершин, количество ребер, список меток по названию графа
    """
    list_of_marks = []
    for edge in graph.edges:
        list_of_marks.append((edge, graph.edges[edge]["label"]))
    return (graph.number_of_nodes(), graph.number_of_edges(), list_of_marks)


def regex_to_dfa(regex: str) -> dfa.DeterministicFiniteAutomaton:
    return re.Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> ndfa.NondeterministicFiniteAutomaton:
    nfa = ndfa.NondeterministicFiniteAutomaton()

    _, _, edges_labels = get_nvertex_nedges_numerate_marks_from_graph(graph)

    if len(start_states) == 0 and len(final_states) == 0:

        for node in graph.nodes():
            start_states.add(node)

        for node in graph.nodes():
            final_states.add(node)

    for state in start_states:
        nfa.add_start_state(State(state))

    for state in final_states:
        nfa.add_final_state(State(state))

    for edge, label in edges_labels:
        state_left = State(edge[0])
        state_right = State(edge[1])
        nfa.add_transition(state_left, label, state_right)

    return nfa
