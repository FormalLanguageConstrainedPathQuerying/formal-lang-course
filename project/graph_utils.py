from dataclasses import dataclass

from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol

import cfpq_data

__all__ = [
    "GraphData",
    "from_named_graph_to_graph_data",
    "write_labeled_two_cycles_graph_as_dot",
    "from_graph_to_nfa",
    "regular_path_query"
]

from pyformlang.regular_expression import Regex

from project.automata_utils import from_regex_to_dfa, intersect_enfa, boolean_decompose_enfa


@dataclass
class GraphData:
    number_of_nodes: int
    number_of_edges: int
    labels: set[str]


def from_graph_to_graph_data(graph: MultiDiGraph) -> GraphData:
    return GraphData(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([edge[2]["label"] for edge in graph.edges(data=True)]),
    )


def from_named_graph_to_graph_data(name: str) -> GraphData:
    """
    Extracts graph data from named graph inside CFPQ Data Dataset

    :param name: name of graph to find in CFPQ Data Dataset
    :return: GraphData object filled with named graph data
    :raises FileNotFoundError: if graph with given name not found inside CFPQ Data Dataset
    """
    path = cfpq_data.dataset.download(name)
    return from_graph_to_graph_data(cfpq_data.graph_from_csv(path))


def write_labeled_two_cycles_graph_as_dot(
        sizes: tuple[int, int], labels: tuple[str, str], path: str
):
    """
    Generates cfpq_data.labeled_two_cycles_graph in file with given sizes of cycles and given labels on edges

    :param sizes: sizes for each cycle
    :param labels: labels for edges in each cycle
    :param path: output path where graph will be written in DOT format
    """
    n, m = sizes
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    write_dot(graph, path)


def from_graph_to_nfa(
        graph: MultiDiGraph, start_states: list[any] = None, final_states: list[any] = None
) -> EpsilonNFA:
    """
    Generates epsilon NFA from given graph

    :param graph: graph to be converted (edges must be marked with "label")
    :param start_states: start states in generated NFA
    :param final_states: final states in generated NFA
    :return: EpsilonNFA object representing NFA from given graph
    """
    enfa = EpsilonNFA()

    for u, v, ddict in graph.edges(data=True):
        label = ddict["label"]
        enfa.add_transition(State(u), Symbol(label), State(v))

    for node in graph.nodes:
        if not start_states or node in start_states:
            enfa.add_start_state(State(node))
        if not final_states or node in final_states:
            enfa.add_final_state(State(node))

    return enfa


def regular_path_query(regex: Regex, graph: MultiDiGraph, start_states: list[any] = None,
                       final_states: list[any] = None) -> set[tuple[any, any]]:
    """
    Performs rpq (regular path query) in graph with regex
    :param regex: regex to define regular path query
    :param graph: graph to be inspected
    :param start_states: start nodes to rpq inside graph
    :param final_states: final nodes to rpq inside graph
    :return: 2 element tuples with nodes satisfying rpq
    """
    if start_states is None:
        start_states = list(graph.nodes)

    if final_states is None:
        final_states = list(graph.nodes)

    graph_as_enfa = from_graph_to_nfa(graph, start_states, final_states)
    regex_as_enfa = from_regex_to_dfa(regex)
    intersection_enfa = intersect_enfa(graph_as_enfa, regex_as_enfa)

    boolean_decompose_intersection = boolean_decompose_enfa(intersection_enfa)
    intersection_states = boolean_decompose_intersection.states()
    transitive_closure_of_intersection = boolean_decompose_intersection.transitive_closure()
    transitive_closure_connected_states = zip(*transitive_closure_of_intersection.nonzero())
    results = set()
    for (i, j) in transitive_closure_connected_states:
        (graph_start_state, regex_start_state) = intersection_states[i].value
        (graph_final_state, regex_final_state) = intersection_states[j].value
        if graph_start_state in start_states and graph_final_state in final_states \
                and regex_start_state in regex_as_enfa.start_states and regex_final_state in regex_as_enfa.final_states:
            results.add((graph_start_state, graph_final_state))

    return results
