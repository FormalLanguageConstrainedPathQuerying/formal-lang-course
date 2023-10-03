from pyformlang.finite_automaton import FiniteAutomaton
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix, coo_array
from project.rpq.utils import boolean_decomposition
from project.automaton_utils import regex_to_dfa


def direct_sum(matrix1: csr_matrix, matrix2: csr_matrix) -> np.ndarray:
    dsum = np.zeros(np.add(matrix1.get_shape(), matrix2.get_shape()))
    print(type(matrix1.get_shape()[0]))
    dsum[: matrix1.get_shape()[0], : matrix1.get_shape()[1]] = matrix1.todense()
    dsum[matrix1.get_shape()[0] :, matrix1.get_shape()[1] :] = matrix2.todense()
    return dsum


def extract_left_submatrix(matrix: np.ndarray, number_of_states: int) -> np.ndarray:
    return matrix[:, :number_of_states]


def extract_right_submatrix(matrix: np.ndarray, number_of_states: int) -> np.ndarray:
    return matrix[:, number_of_states:]


def prepare_M(
    graph_nodes: list,
    reg_states: list,
    start_nodes: list,
    start_states: list,
    task_type: int = 1,
) -> np.ndarray:
    assert task_type == 1 or task_type == 2
    number_of_nodes = len(graph_nodes)
    number_of_start_nodes = len(start_nodes)
    number_of_states = len(reg_states)
    if task_type == 1:
        M = np.zeros((number_of_states, number_of_states + number_of_nodes))
        M[:, :number_of_states] = np.eye(number_of_states)
        for start_state in start_states:
            row = reg_states.index(start_state)
            for start_node in start_nodes:
                M[row, number_of_states + graph_nodes.index(start_node)] = 1
    else:
        M = np.zeros(
            (
                number_of_states * number_of_start_nodes,
                number_of_states + number_of_nodes,
            )
        )
        for i in range(number_of_start_nodes):
            base = i * number_of_states
            M[base : base + number_of_states, :number_of_states] = np.eye(
                number_of_states
            )
            for start_state in start_states:
                row = reg_states.index(start_state)
                M[base + row, number_of_states + graph_nodes.index(start_nodes[i])] = 1
    return M


def bfs_graph_reg_automaton(
    graph: nx.MultiDiGraph,
    reg_automaton: FiniteAutomaton,
    start_nodes: set,
    final_nodes: set = set(),
    task_type: int = 1,
) -> set[tuple] | dict[set]:
    """
    Type 1: For the specified set of starting nodes, find the set of reachable ones.
    Type 2: For each node from the specified set, find the set of reachable ones.
    """
    assert task_type == 1 or task_type == 2

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

    M = prepare_M(graph_nodes, reg_states, start_nodes, start_states, task_type)
    M_last = None

    while not (M_last == M).all():
        M_last = M.copy()
        M_right = extract_right_submatrix(M, number_of_states).copy()
        for label in shared_labels:
            M_label = np.minimum(np.matmul(M, direct_sums[label]), 1)
            left_submatrix = coo_matrix(
                extract_left_submatrix(M_label, number_of_states)
            )
            right_submatrix = extract_right_submatrix(M_label, number_of_states)
            for i, j in zip(left_submatrix.row, left_submatrix.col):
                M_right[
                    (i // number_of_states) * number_of_states + j
                ] += right_submatrix[i]
        M_right = np.minimum(M_right, 1)
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
    if task_type == 1:
        result = get_reachable(right_submatrix)
    else:
        result = {}
        for i in range(len(start_nodes)):
            base = i * number_of_states
            result[start_nodes[i]] = get_reachable(
                right_submatrix[base : base + number_of_states, :]
            )

    return result


def bfs_rpq(
    graph: nx.MultiDiGraph,
    regex: str,
    start_nodes: set,
    final_nodes: set = set(),
    task_type: int = 1,
) -> set[tuple] | dict[set]:
    return bfs_graph_reg_automaton(
        graph, regex_to_dfa(regex), start_nodes, final_nodes, task_type
    )
