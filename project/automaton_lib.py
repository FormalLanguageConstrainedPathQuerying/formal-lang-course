from typing import List, Optional

import numpy as np
import networkx as nx

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from scipy.sparse import csr_array
from scipy.sparse import kron
from project.matrix.automaton_binary_matrix import AutomatonBinaryMatrix
from project.graph_lib import get_graph_data


def dfa_of_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Creates deterministic finite automaton from regex

    Args:
        regex: Regular expression to generate DFA from

    Returns:
        Minimal deterministic finite automaton
    """
    return regex.to_epsilon_nfa().minimize()


def nfa_of_graph(
    graph: nx.MultiDiGraph,
    starting_nodes: Optional[List[int]] = None,
    final_nodes: Optional[List[int]] = None,
) -> NondeterministicFiniteAutomaton:
    """
    Creates nondeterministic finite automaton from networkx MultiDiGraph

    Args:
        graph: Graph to make automaton from
        To indicate starting node, "is_start" data should be set to True
        To indicate final node, "is_final" data should be set to True
        Data "label" is needed for transition to be valid
        Starting and final nodes will be overriden if starting_nodes or
        final_nodes will be supplied respectively

        starting_nodes: List of starting nodes
        Overrides is_start from the graph given

        final_nodes: List of final nodes
        Overrides is_final from the graph given

    Returns:
        Generated nondeterministic finite automaton
    """

    graph = graph.copy()

    if starting_nodes is not None:
        nx.set_node_attributes(
            graph, {i: i in starting_nodes for i in graph.nodes}, name="is_start"
        )
    else:
        nx.set_node_attributes(graph, {i: True for i in graph.nodes}, name="is_start")

    if final_nodes is not None:
        nx.set_node_attributes(
            graph, {i: i in final_nodes for i in graph.nodes}, name="is_final"
        )
    else:
        nx.set_node_attributes(graph, {i: True for i in graph.nodes}, name="is_final")

    automaton = NondeterministicFiniteAutomaton.from_networkx(graph)
    automaton = automaton.remove_epsilon_transitions()

    return automaton


def graph_of_matrices(matrices: List[AutomatonBinaryMatrix]) -> nx.MultiDiGraph:
    """
    Create graph from list of binary matrices

    Args:
        matrices: Automaton binary matrices to create graph from

    Returns:
        Built MultDiGraph
    """
    assert len(matrices) > 0, "Need at least 1 matrix"

    graph = nx.MultiDiGraph()

    for node in matrices[0].nodes:
        graph.add_node(node)

    for matrix in matrices:
        for i in range(len(matrices[0].nodes)):
            for j in range(len(matrices[0].nodes)):
                if matrix.matrix.getrow(i)[0, j]:
                    graph.add_edge(
                        matrices[0].nodes[i], matrices[0].nodes[j], label=matrix.label
                    )

    return graph


def transitive_closure(matrix: csr_array) -> csr_array:
    """
    Calculates transitive closure of binary matrix represented in CSR Array form

    Args:
        matrix: CSR Array matrix to calculate transitive closure of

    Returns:
        Transitive closure of matrix
    """
    transitive_closure = matrix

    nonzero_count = transitive_closure.count_nonzero()
    current_nonzero_count = 0

    while current_nonzero_count != nonzero_count:
        transitive_closure += transitive_closure @ transitive_closure
        nonzero_count = current_nonzero_count
        current_nonzero_count = transitive_closure.count_nonzero()

    return transitive_closure


def binary_matrix_of_automaton(
    automaton: NondeterministicFiniteAutomaton, label: str
) -> AutomatonBinaryMatrix:
    """
    Creates binary matrix representation of automaton for the label given

    Args:
        automaton: Nondeterministic finite automaton to make representation of
        label: transition for the binary matrix

    Returns:
        Binary matrix representation of automaton for the label given
    """

    states = list(map(lambda x: x.value, automaton.states))
    matrix = csr_array((len(states), len(states)), dtype=np.bool_)
    automaton_dict = automaton.to_dict()
    transitions = []

    for starting_node in automaton_dict:
        for transition_symbol in automaton_dict[starting_node]:
            if transition_symbol != label:
                continue

            final_symbols = automaton_dict[starting_node][transition_symbol]

            if final_symbols is set:
                for final_symbol in final_symbols:
                    transitions.append((starting_node, transition_symbol, final_symbol))
            else:
                transitions.append((starting_node, transition_symbol, final_symbols))

    for edge in transitions:
        state_from, _, state_to = edge
        if type(state_to) == set:
            for state in state_to:
                x, y = states.index(state_from.value), states.index(state.value)
        else:
            x, y = states.index(state_from.value), states.index(state_to.value)
        matrix[x, y] = True

    start_states = set(filter(lambda x: x != "\\n", automaton.start_states))
    final_states = set(filter(lambda x: x != "\\n", automaton.final_states))

    return AutomatonBinaryMatrix(matrix, start_states, final_states, states, label)


def binary_matrices_of_automaton(
    automaton: NondeterministicFiniteAutomaton,
) -> List[AutomatonBinaryMatrix]:
    """
    Creates set of binary matrix representations of automaton for all labels

    Args:
        automaton: Nondeterministic finite automaton to make representations of

    Returns:
        Set of binary matrix representations of automaton
    """

    matrices = list()
    labels = get_graph_data(automaton.to_networkx()).labels
    labels = filter(lambda x: x is not None and x != "\\n", labels)

    for label in labels:
        matrices.append(binary_matrix_of_automaton(automaton, label))

    return matrices


def automaton_of_binary_matrices(
    matrices: List[AutomatonBinaryMatrix],
) -> NondeterministicFiniteAutomaton:
    """
    Converts a list of binary matrices to automaton

    Args:
        matrices: list of binary matrices to create automaton from

    Returns:
        Built automaton
    """
    graph = graph_of_matrices(matrices)
    automaton = nfa_of_graph(graph)
    return automaton


def intersect_automatons(
    first: NondeterministicFiniteAutomaton, second: NondeterministicFiniteAutomaton
) -> NondeterministicFiniteAutomaton:
    """
    Creates an automaton from intersecting two others using binary matrices

    Args:
        first: first automaton
        secont: second automaton

    Returns:
        intersection of first and second automaton
    """
    first_matrices = binary_matrices_of_automaton(first)
    second_matrices = binary_matrices_of_automaton(second)

    first_size = len(first_matrices[0].nodes)
    second_size = len(second_matrices[0].nodes)

    result_nodes = []
    result_final = []
    result_starting = []
    result_matrices = dict()

    labels = set(map(lambda x: x.label, first_matrices)).union(
        set(map(lambda x: x.label, second_matrices))
    )

    for label in labels:
        first_matrix = list(filter(lambda x: x.label == label, first_matrices))
        first_matrix = (
            first_matrix[0]
            if len(first_matrix)
            else csr_array((first_size, first_size))
        )
        second_matrix = list(filter(lambda x: x.label == label, second_matrices))
        second_matrix = (
            second_matrix[0]
            if len(second_matrix)
            else csr_array((second_size, second_size))
        )
        result_matrices[label] = kron(first_matrix.matrix, second_matrix.matrix)

    for first_node in first_matrices[0].nodes:
        for second_node in second_matrices[0].nodes:
            new_node = "(" + first_node + ", " + second_node + ")"
            result_nodes.append(new_node)

            if (
                first_node in first_matrices[0].starting_nodes
                and second_node in second_matrices[0].starting_nodes
            ):
                result_starting.append(new_node)

            if (
                first_node in first_matrices[0].final_nodes
                and second_node in second_matrices[0].final_nodes
            ):
                result_starting.append(new_node)

    result_binary_matrices = []

    for label in result_matrices.keys():
        result_binary_matrices.append(
            AutomatonBinaryMatrix(
                result_matrices[label],
                result_starting,
                result_final,
                result_nodes,
                label,
            )
        )

    intersection = automaton_of_binary_matrices(result_binary_matrices)
    return intersection


def regular_request(
    graph: nx.MultiDiGraph, start_nodes: List[str], final_nodes: List[str], regex: Regex
) -> set:
    nfa = nfa_of_graph(graph, start_nodes, final_nodes)
    dfa = dfa_of_regex(regex)

    intersection_matrices = binary_matrices_of_automaton(intersect_automatons(nfa, dfa))
    intersection_matrix = sum(map(lambda x: x.matrix, intersection_matrices))

    transitive_closure_res = transitive_closure(intersection_matrix)

    nodes = intersection_matrices[0].nodes

    result = set()

    for start_node in nodes:
        for final_node in nodes:
            final_index = nodes.index(final_node)
            start_index = nodes.index(start_node)

            nfa_start_node = start_node.split(",")[0].replace("(", "")
            nfa_final_node = final_node.split(",")[0].replace("(", "")

            if (
                transitive_closure_res.getrow(start_index)[0, final_index]
                and nfa_start_node in start_nodes
                and nfa_final_node in final_nodes
            ):
                result.add((nfa_start_node, nfa_final_node))

    return result
