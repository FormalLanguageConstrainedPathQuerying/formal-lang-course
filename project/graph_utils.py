import cfpq_data

from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
)
from networkx import MultiDiGraph, nx_pydot
from dataclasses import dataclass
from typing import Set, Tuple


@dataclass
class Graph:
    node_count: int
    edge_count: int
    edge_labels: Set[str]


def load_graph(graph_name: str) -> MultiDiGraph:
    path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path)

    return graph


def get_graph(graph_name: str) -> Graph:
    graph = load_graph(graph_name)

    return Graph(
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        edge_labels=set(cfpq_data.get_sorted_labels(graph)),
    )


def create_labeled_two_cycles_graph(
    first_cycle_node_count: int,
    second_cycle_node_count: int,
    labels: Tuple[str, str],
    save_path: str = "",
) -> MultiDiGraph:
    graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_node_count, second_cycle_node_count, labels=labels
    )
    if save_path:
        save_graph_to_dot(graph, save_path)

    return graph


def save_graph_to_dot(graph: MultiDiGraph, dot_path: str) -> None:
    nx_pydot.write_dot(graph, dot_path)


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa: NondeterministicFiniteAutomaton = (
        NondeterministicFiniteAutomaton.from_networkx(
            graph
        ).remove_epsilon_transitions()
    )
    all_nodes = [int(node) for node in graph.nodes]

    start_states = start_states if start_states else all_nodes
    final_states = final_states if final_states else all_nodes

    for st in start_states:
        nfa.add_start_state(State(st))

    for st in final_states:
        nfa.add_final_state(State(st))

    return nfa
