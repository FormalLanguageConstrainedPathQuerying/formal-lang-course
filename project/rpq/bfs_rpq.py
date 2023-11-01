from pyformlang.finite_automaton import FiniteAutomaton
import networkx as nx
import numpy as np
from scipy.sparse import eye, lil_matrix, coo_array
from project.rpq.graph_operations import boolean_decomposition
from project.automaton_utils import str_regex_to_dfa


def direct_sum(matrix1: lil_matrix, matrix2: lil_matrix) -> lil_matrix:
    dsum = lil_matrix(tuple(np.add(matrix1.get_shape(), matrix2.get_shape())))
    dsum[: matrix1.get_shape()[0], : matrix1.get_shape()[1]] = matrix1
    dsum[matrix1.get_shape()[0] :, matrix1.get_shape()[1] :] = matrix2
    return dsum


def extract_left_submatrix(matrix: lil_matrix, number_of_states: int) -> lil_matrix:
    return matrix[:, :number_of_states]


def extract_right_submatrix(matrix: lil_matrix, number_of_states: int) -> lil_matrix:
    return matrix[:, number_of_states:]


def bfs_graph_reg_all(
    graph: nx.MultiDiGraph,
    reg_automaton: FiniteAutomaton,
    start_nodes: set,
    final_nodes: set = set(),
) -> set[tuple]:
    if len(final_nodes) == 0:
        final_nodes = graph.nodes

    start_nodes = list(start_nodes)  # Required to fix the order of start_nodes
    start_states = list(reg_automaton.start_states)
    for start_state in start_states:
        reg_automaton.remove_start_state(start_state)

    reg_graph = reg_automaton.to_networkx()
    graph_nodes = list(graph.adj.keys())
    reg_states = list(reg_graph.adj.keys())
    number_of_states = len(reg_states)

    graph_boolean_decomposition = boolean_decomposition(graph)
    reg_boolean_decomposition = boolean_decomposition(reg_graph)

    shared_labels = set(graph_boolean_decomposition.keys()) & set(
        reg_boolean_decomposition.keys()
    )
    direct_sums = {}
    for label in shared_labels:
        direct_sums[label] = direct_sum(
            reg_boolean_decomposition[label], graph_boolean_decomposition[label]
        )

    number_of_nodes = len(graph_nodes)
    number_of_states = len(reg_states)
    M = lil_matrix((number_of_states, number_of_states + number_of_nodes))
    M[:, :number_of_states] = eye(number_of_states)
    for start_state in start_states:
        row = reg_states.index(start_state)
        for start_node in start_nodes:
            M[row, number_of_states + graph_nodes.index(start_node)] = 1
    M_last = lil_matrix(M.get_shape())

    while (M_last - M).count_nonzero() != 0:
        M_last = M.copy()
        M_right = extract_right_submatrix(M, number_of_states).copy()
        for label in shared_labels:
            M_label = (M @ direct_sums[label]).minimum(1)
            left_submatrix = lil_matrix(
                extract_left_submatrix(M_label, number_of_states)
            )
            right_submatrix = extract_right_submatrix(M_label, number_of_states)
            rows, cols = left_submatrix.nonzero()
            for i, j in zip(rows, cols):
                M_right[
                    (i // number_of_states) * number_of_states + j
                ] += right_submatrix[i]
        M_right = M_right.minimum(1)
        M[:, number_of_states:] = M_right

    right_submatrix = extract_right_submatrix(M, number_of_states)
    result = set()
    for final_state in reg_automaton.final_states:
        for i in coo_array(right_submatrix[reg_states.index(final_state)]).col:
            node = graph_nodes[i]
            if node not in start_nodes and node in final_nodes:
                result.add(node)

    return result


def bfs_graph_reg_foreach(
    graph: nx.MultiDiGraph,
    reg_automaton: FiniteAutomaton,
    start_nodes: set,
    final_nodes: set = set(),
) -> dict[set]:
    if len(final_nodes) == 0:
        final_nodes = graph.nodes

    start_nodes = list(start_nodes)  # Required to fix the order of start_nodes
    start_states = list(reg_automaton.start_states)
    for start_state in start_states:
        reg_automaton.remove_start_state(start_state)

    reg_graph = reg_automaton.to_networkx()
    graph_nodes = list(graph.adj.keys())
    reg_states = list(reg_graph.adj.keys())
    number_of_states = len(reg_states)

    graph_boolean_decomposition = boolean_decomposition(graph)
    reg_boolean_decomposition = boolean_decomposition(reg_graph)

    shared_labels = set(graph_boolean_decomposition.keys()) & set(
        reg_boolean_decomposition.keys()
    )
    direct_sums = {}
    for label in shared_labels:
        direct_sums[label] = direct_sum(
            reg_boolean_decomposition[label], graph_boolean_decomposition[label]
        )

    number_of_nodes = len(graph_nodes)
    number_of_start_nodes = len(start_nodes)
    number_of_states = len(reg_states)
    M = lil_matrix(
        (
            number_of_states * number_of_start_nodes,
            number_of_states + number_of_nodes,
        )
    )
    for i in range(number_of_start_nodes):
        base = i * number_of_states
        M[base : base + number_of_states, :number_of_states] = eye(number_of_states)
        for start_state in start_states:
            row = reg_states.index(start_state)
            M[base + row, number_of_states + graph_nodes.index(start_nodes[i])] = 1
    M_last = lil_matrix(M.get_shape())

    while (M_last - M).count_nonzero() != 0:
        M_last = M.copy()
        M_right = extract_right_submatrix(M, number_of_states).copy()
        for label in shared_labels:
            M_label = (M @ direct_sums[label]).minimum(1)
            left_submatrix = lil_matrix(
                extract_left_submatrix(M_label, number_of_states)
            )
            right_submatrix = extract_right_submatrix(M_label, number_of_states)
            rows, cols = left_submatrix.nonzero()
            for i, j in zip(rows, cols):
                M_right[
                    (i // number_of_states) * number_of_states + j
                ] += right_submatrix[i]
        M_right = M_right.minimum(1)
        M[:, number_of_states:] = M_right

    def get_reachable(matrix):
        reachable = set()
        for final_state in reg_automaton.final_states:
            for i in coo_array(matrix[reg_states.index(final_state)]).col:
                node = graph_nodes[i]
                if node not in start_nodes and node in final_nodes:
                    reachable.add(node)
        return reachable

    right_submatrix = extract_right_submatrix(M, number_of_states)
    result = {}
    for i in range(len(start_nodes)):
        base = i * number_of_states
        result[start_nodes[i]] = get_reachable(
            right_submatrix[base : base + number_of_states, :]
        )

    return result


def bfs_rpq_all(
    graph: nx.MultiDiGraph, regex: str, start_nodes: set, final_nodes: set = set()
) -> set[tuple]:
    return bfs_graph_reg_all(graph, str_regex_to_dfa(regex), start_nodes, final_nodes)


def bfs_rpq_foreach(
    graph: nx.MultiDiGraph, regex: str, start_nodes: set, final_nodes: set = set()
) -> dict[set]:
    return bfs_graph_reg_foreach(
        graph, str_regex_to_dfa(regex), start_nodes, final_nodes
    )
