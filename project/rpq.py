from typing import Set, Dict, Iterable

from scipy import sparse
import networkx as nx

import project.regex_util as regex_util
from project.matrix_util import AdjacencyMatrix, intersect_adjacency_matrices, _get_front, _get_reachable_states


def rpq_to_graph_tc(graph: nx.MultiDiGraph, query: str, start_nodes: set = None, final_nodes: set = None) -> set:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with transitive closure method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Query as set
    """
    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    intersected_matrix = intersect_adjacency_matrices(graph_matrix, query_matrix)
    transitive_closure = intersected_matrix.get_transitive_closure()
    start_states = intersected_matrix.start_states
    final_states = intersected_matrix.final_states

    result = set()
    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result.add((state_from // query_matrix.get_states_len(), state_to // query_matrix.get_states_len()))
    return result


def rpq_to_graph_bfs(
        graph: nx.MultiDiGraph, query: str, start_nodes: Iterable[int] = None, final_nodes: Iterable[int] = None
) -> Set[int]:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with BFS method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Querying in Set format
    """

    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    symbols = graph_matrix.matrix.keys().__and__(query_matrix.matrix.keys())
    front = (
        sparse.vstack(
            [_get_front(graph_matrix, query_matrix, {i}) for i in map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)]
        )
    )
    visited_matrix = front

    while True:
        new_front = sparse.csr_matrix(front.shape, dtype=bool)
        for label in symbols:
            next_front_part = front.__matmul__(graph_matrix.matrix[label])
            for (i, j) in zip(*query_matrix.matrix[label].nonzero()):
                new_front[ j, :] += next_front_part[ i, :]

        front = new_front > visited_matrix
        visited_matrix += front

        if front.count_nonzero() == 0:
            break

    result = _get_reachable_states(graph_matrix, query_matrix, 0, visited_matrix)
    return {end.value for end in result}


def rpq_to_graph_bfs_all_reachable(
        graph: nx.MultiDiGraph, query: str, start_nodes: Iterable[int] = None, final_nodes: Iterable[int] = None
) -> Dict[int, Set[int]]:
    """
    Calculates Regular Path Querying (RPQ) for graph and regular expression with BFS method
    :param graph: Graph to send query to
    :param query: Regular Expression to query
    :param start_nodes: Set of start nodes
    :param final_nodes: Set of final nodes
    :return: Regular Path Querying in Dictionary format
    """

    nfa = regex_util.graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_util.regex_to_min_dfa(query)
    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)
    symbols = graph_matrix.matrix.keys().__and__(query_matrix.matrix.keys())
    front = (
        sparse.vstack(
            [_get_front(graph_matrix, query_matrix, {i}) for i in map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)]
        )
    )
    visited_matrix = front

    while True:
        new_front = sparse.csr_matrix(front.shape, dtype=bool)
        for label in symbols:
            new_front_cut = front.__matmul__(graph_matrix.matrix[label])
            for index in range(len(graph_matrix.start_states)):
                for (i, j) in zip(*query_matrix.matrix[label].nonzero()):
                    new_front[index * query_matrix.get_states_len() + j, :] += \
                        new_front_cut[index * query_matrix.get_states_len() + i, :]

        front = new_front > visited_matrix
        visited_matrix += front

        if front.count_nonzero() == 0:
            break

    result = {
        graph_matrix.state_by_index(start_state_idx):
            _get_reachable_states(graph_matrix, query_matrix, sub_front_idx, visited_matrix)
            for sub_front_idx, start_state_idx in enumerate(
                map(lambda state: graph_matrix.index_by_state(state), graph_matrix.start_states)
            )
        }

    return {start.value: {end.value for end in ends} for (start, ends) in result.items()}

