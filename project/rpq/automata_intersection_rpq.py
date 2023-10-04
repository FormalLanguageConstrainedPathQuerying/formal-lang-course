from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
import networkx as nx
from project.automaton_utils import *
from scipy.sparse import kron
from project.rpq.graph_operations import boolean_decomposition


def automata_intersection(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    start_states1 = list(automaton1.start_states)
    start_states2 = list(automaton2.start_states)
    for start_state in start_states1:
        automaton1.remove_start_state(start_state)
    for start_state in start_states2:
        automaton2.remove_start_state(start_state)
    graph1, graph2 = automaton1.to_networkx(), automaton2.to_networkx()
    graph_states1 = list(graph1.adj.keys())
    graph_states2 = list(graph2.adj.keys())
    boolean_decomposition1 = boolean_decomposition(graph1)
    boolean_decomposition2 = boolean_decomposition(graph2)
    shared_labels = set(boolean_decomposition1.keys()) & set(
        boolean_decomposition2.keys()
    )
    intersection = NondeterministicFiniteAutomaton(
        [
            State((state1, state2))
            for state2 in automaton2.states
            for state1 in automaton1.states
        ]
    )
    for label in shared_labels:
        kronecker_product = kron(
            boolean_decomposition1[label], boolean_decomposition2[label]
        ).tocoo()
        for start_vertex, end_vertex in zip(
            kronecker_product.row, kronecker_product.col
        ):
            start_state1 = graph_states1[
                start_vertex // boolean_decomposition2[label].get_shape()[0]
            ]
            start_state2 = graph_states2[
                start_vertex % boolean_decomposition2[label].get_shape()[0]
            ]
            end_state1 = graph_states1[
                end_vertex // boolean_decomposition2[label].get_shape()[1]
            ]
            end_state2 = graph_states2[
                end_vertex % boolean_decomposition2[label].get_shape()[1]
            ]
            intersection.add_transition(
                State((start_state1, start_state2)),
                Symbol(label),
                State((end_state1, end_state2)),
            )
    for start_state1 in start_states1:
        for start_state2 in start_states2:
            intersection.add_start_state(State((start_state1, start_state2)))
    for final_state1 in automaton1.final_states:
        for final_state2 in automaton2.final_states:
            intersection.add_final_state(State((final_state1, final_state2)))
    return intersection


def automata_intersection_rpq(
    graph: nx.MultiDiGraph,
    regex: str,
    start_nodes: set = set(),
    final_nodes: set = set(),
) -> set[tuple]:
    graph_automaton = graph_to_nfa(graph, start_nodes, final_nodes)
    graph = graph_automaton.to_networkx()
    regex_automaton = regex_to_dfa(regex)
    adjacency_matrix = nx.adjacency_matrix(graph)
    previous_count_nonzero = None
    nonterminal = Symbol("NONTERMINAL")
    while adjacency_matrix.count_nonzero() != previous_count_nonzero:
        previous_count_nonzero = adjacency_matrix.count_nonzero()
        intersection = automata_intersection(
            graph_automaton.copy(), regex_automaton.copy()
        )
        intersection_graph = intersection.to_networkx()
        intersection_adjacency_matrix = nx.adjacency_matrix(intersection_graph).tolil()
        transitive_closure = nx.transitive_closure(intersection_graph, None)
        transitive_closure_states = list(transitive_closure.adj.keys())
        transitive_closure_matrix = nx.adjacency_matrix(transitive_closure).tocoo()
        for i, j in zip(transitive_closure_matrix.row, transitive_closure_matrix.col):
            state1 = transitive_closure_states[i]
            state2 = transitive_closure_states[j]
            if (
                intersection_adjacency_matrix[i, j] == 0
                and state1[1] in regex_automaton.start_states
                and state2[1] in regex_automaton.final_states
            ):
                graph_automaton.add_transition(
                    State(state1[0]), nonterminal, State(state2[0])
                )
        adjacency_matrix = nx.adjacency_matrix(graph_automaton.to_networkx())

    adjacency_matrix = adjacency_matrix.tocoo()
    graph_states = list(graph.adj.keys())
    ignore_indexes = [
        i
        for i in range(len(graph_states))
        if graph_states[i] not in graph_automaton.states
    ]
    result = set()
    for i, j in zip(adjacency_matrix.row, adjacency_matrix.col):
        if i in ignore_indexes or j in ignore_indexes:
            continue
        state1, state2 = graph_states[i], graph_states[j]
        if (
            state1 in graph_automaton.start_states
            and state2 in graph_automaton.final_states
        ):
            result.add((state1, state2))
    return result
