from typing import Union

import networkx as nx
from pyformlang.regular_expression import Regex
from scipy import sparse

from project.boolean_decompositon import BooleanDecomposition
from project.regex_utils import create_nfa_from_graph, regex_to_dfa
from scipy.sparse import csr_matrix


def rpq_bfs(
    graph: nx.MultiDiGraph,
    regex: Regex,
    start_states: set = None,
    final_states: set = None,
    is_for_each: bool = False,
) -> set:
    if len(start_states) == 0 or len(final_states) == 0:
        return set()

    graph_bool_decomposition = BooleanDecomposition(
        create_nfa_from_graph(graph, start_states, final_states)
    )
    regex_bool_decomposition = BooleanDecomposition(regex_to_dfa(regex))
    result = bfs_sync(
        graph_bool_decomposition,
        regex_bool_decomposition,
        is_for_each,
        start_states,
        final_states,
    )

    return (
        {(start.value, end.value) for (start, ends) in result.items() for end in ends}
        if is_for_each
        else {end.value for end in result}
    )


def _get_reachable_nodes(
    sub_front_indexes,
    graph: BooleanDecomposition,
    regex: BooleanDecomposition,
    visited,
) -> set:
    sub_front_padding = sub_front_indexes * regex.states_num
    reachable = sparse.csr_matrix((1, graph.states_num), dtype=bool)
    for i in map(lambda state: regex.get_index(state), regex.get_final_states()):
        reachable += visited[sub_front_padding + i, :]
    return set(
        graph.state_by_index(i)
        for i in reachable.nonzero()[1]
        if i in map(lambda state: graph.get_index(state), graph.get_final_states())
    )


def bfs_sync(
    graph: BooleanDecomposition,
    regex: BooleanDecomposition,
    is_for_each: bool = False,
    start_states: set = None,
    final_states: set = None,
) -> Union[set, dict]:
    if len(graph.get_states()) == 0 or len(start_states) == 0 or len(final_states) == 0:
        return dict() if is_for_each else set()

    common_symbols = graph.bool_decomposition.keys() & (regex.bool_decomposition.keys())
    front = (
        sparse.vstack(
            [
                _create_front(graph, regex, {i})
                for i in map(
                    lambda state: graph.get_index(state),
                    graph.get_start_states(),
                )
            ]
        )
        if is_for_each
        else _create_front(
            graph,
            regex,
            map(
                lambda state: graph.get_index(state),
                graph.get_start_states(),
            ),
        )
    )

    visited = front
    while True:
        next_front = sparse.csr_matrix(front.shape, dtype=bool)
        for label in common_symbols:
            next_front_part = front * (graph.bool_decomposition[label])
            for index in range(len(graph.get_start_states()) if is_for_each else 1):
                padding = index * regex.states_num
                for (i, j) in zip(*regex.bool_decomposition[label].nonzero()):
                    next_front[padding + j, :] += next_front_part[padding + i, :]
        front = next_front > visited
        visited += front
        if front.count_nonzero() == 0:
            break

    return (
        {
            graph.state_by_index(start_state_idx): _get_reachable_nodes(
                sub_front_indexes, graph, regex, visited
            )
            for sub_front_indexes, start_state_idx in enumerate(
                map(
                    lambda state: graph.get_index(state),
                    graph.get_start_states(),
                )
            )
        }
        if is_for_each
        else _get_reachable_nodes(0, graph, regex, visited)
    )


def _create_front(
    graph: BooleanDecomposition, regex: BooleanDecomposition, start_states
) -> csr_matrix:
    front_row = sparse.dok_matrix((1, graph.states_num), dtype=bool)

    for i in start_states:
        front_row[0, i] = True
    front_row = front_row.tocsr()

    front = sparse.csr_matrix((regex.states_num, graph.states_num), dtype=bool)

    for i in map(lambda state: regex.get_index(state), regex.get_start_states()):
        front[i, :] = front_row

    return front
