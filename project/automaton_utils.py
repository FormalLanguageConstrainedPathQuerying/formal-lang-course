from pyformlang.finite_automaton import (
    FiniteAutomaton,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.regular_expression import Regex
import networkx as nx


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().remove_epsilon_transitions().minimize()


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_nodes: set = set(), final_nodes: set = set()
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if len(start_nodes) == 0:
        start_nodes = graph.nodes
    if len(final_nodes) == 0:
        final_nodes = graph.nodes
    for start_state in start_nodes:
        nfa.add_start_state(State(start_state))
    for final_state in final_nodes:
        nfa.add_final_state(State(final_state))
    return nfa


def collect_labels_set(graph, start_state, end_state):
    # It is assumed that `start_state` key exists in `graph` and `end_state` key exists in graph[start_state]
    labels_set = set()
    labels_dict = graph[start_state][end_state]
    for key in labels_dict:
        if "label" in labels_dict[key]:
            labels_set.add(labels_dict[key]["label"])
    return labels_set


def automata_intersection(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    states1, states2 = list(automaton1.states), list(automaton2.states)
    graph1, graph2 = automaton1.to_networkx(), automaton2.to_networkx()
    graph_states1 = list(graph1.adj.keys())
    graph_states2 = list(graph2.adj.keys())
    ignore_indexes1 = [
        i
        for i in range(len(graph_states1))
        if str(graph_states1[i]).endswith("_starting")
    ]
    ignore_indexes2 = [
        i
        for i in range(len(graph_states2))
        if str(graph_states2[i]).endswith("_starting")
    ]
    adjacency_matrix1, adjacency_matrix2 = (
        nx.adjacency_matrix(graph1).tocoo(),
        nx.adjacency_matrix(graph2).tocoo(),
    )
    states = [State((state1, state2)) for state2 in states2 for state1 in states1]
    intersection = NondeterministicFiniteAutomaton(states)
    for start1, end1, _ in zip(
        adjacency_matrix1.row, adjacency_matrix1.col, adjacency_matrix1.data
    ):
        if start1 in ignore_indexes1 or end1 in ignore_indexes1:
            continue
        for start2, end2, _ in zip(
            adjacency_matrix2.row, adjacency_matrix2.col, adjacency_matrix2.data
        ):
            if start2 in ignore_indexes2 or end2 in ignore_indexes2:
                continue
            start_state1, start_state2 = graph_states1[start1], graph_states2[start2]
            end_state1, end_state2 = graph_states1[end1], graph_states2[end2]
            for label in collect_labels_set(
                graph1, start_state1, end_state1
            ) & collect_labels_set(graph2, start_state2, end_state2):
                intersection.add_transition(
                    State((start_state1, start_state2)),
                    Symbol(label),
                    State((end_state1, end_state2)),
                )
    start_states = [
        State((i, j)) for j in automaton2.start_states for i in automaton1.start_states
    ]
    final_states = [
        State((i, j)) for j in automaton2.final_states for i in automaton1.final_states
    ]
    for start_state in start_states:
        intersection.add_start_state(start_state)
    for final_state in final_states:
        intersection.add_final_state(final_state)
    return intersection


def automaton_transitive_closure(automaton: FiniteAutomaton) -> nx.Graph:
    return nx.transitive_closure(automaton.to_networkx(), None)


def reachability_problem(
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
    nonterminal = Symbol(None)
    while adjacency_matrix.count_nonzero() != previous_count_nonzero:
        previous_count_nonzero = adjacency_matrix.count_nonzero()
        intersection = automata_intersection(graph_automaton, regex_automaton)
        transitive_closure = automaton_transitive_closure(intersection)
        transitive_closure_states = list(transitive_closure.adj.keys())
        intersection_adjacency_matrix = nx.adjacency_matrix(transitive_closure).tocoo()
        for i, j, _ in zip(
            intersection_adjacency_matrix.row,
            intersection_adjacency_matrix.col,
            intersection_adjacency_matrix.data,
        ):
            state1 = transitive_closure_states[i]
            state2 = transitive_closure_states[j]
            if (
                len(collect_labels_set(transitive_closure, state1, state2)) == 0
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
        if str(graph_states[i]).endswith("_starting")
    ]
    result = set()
    for i, j, _ in zip(
        adjacency_matrix.row, adjacency_matrix.col, adjacency_matrix.data
    ):
        if i in ignore_indexes or j in ignore_indexes:
            continue
        state1, state2 = graph_states[i], graph_states[j]
        if (
            state1 in graph_automaton.start_states
            and state2 in graph_automaton.final_states
        ):
            result.add((state1, state2))
    return result
