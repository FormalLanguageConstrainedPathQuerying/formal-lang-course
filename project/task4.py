from networkx.classes import MultiDiGraph
from pyformlang.finite_automaton import (
    Symbol,
)
from functools import reduce
from scipy.sparse import csr_matrix
from project.task2 import regex_to_dfa, graph_to_nfa
from project.task3 import AdjacencyMatrixFA


def get_start_front(
    fa_regex: AdjacencyMatrixFA, fa_graph: AdjacencyMatrixFA
) -> csr_matrix:
    regex_start_state_i: int = fa_regex.start_states_is[0]
    graph_start_states_count: int = len(fa_graph.start_states_is)

    row = [
        regex_start_state_i + fa_regex.states_count * i
        for i in range(graph_start_states_count)
    ]
    col = [st_state_i for st_state_i in fa_graph.start_states_is]
    data = [True] * graph_start_states_count

    return csr_matrix(
        (data, (row, col)),
        shape=(
            fa_regex.states_count * graph_start_states_count,
            fa_graph.states_count,
        ),
        dtype=bool,
    )


def is_front_not_empty(front: csr_matrix):
    return front.toarray().any()


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    # print(regex, start_nodes, final_nodes)
    # print(graph.nodes, graph.edges)

    fa_regex: AdjacencyMatrixFA = AdjacencyMatrixFA(regex_to_dfa(regex))
    fa_graph: AdjacencyMatrixFA = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )

    # BFS result
    pairs: set[tuple[int, int]] = set()

    regex_transposed_matrices: dict[Symbol, csr_matrix] = {
        sym: m.transpose() for sym, m in fa_regex.sparse_matrices.items()
    }

    # paths for each sym
    fronts: dict[Symbol, csr_matrix] = {}

    # Init front with start states
    global_front: csr_matrix = get_start_front(fa_regex, fa_graph)
    visited: csr_matrix = global_front

    syms = [
        s
        for s in fa_regex.sparse_matrices.keys()
        if s in fa_graph.sparse_matrices.keys()
    ]

    # while we have paths
    while is_front_not_empty(global_front):
        fronts = {}

        for sym in syms:
            # find new front for current sym
            fronts[sym] = global_front @ fa_graph.sparse_matrices[sym]

            for i in range(len(start_nodes)):
                start = i * fa_regex.states_count
                end = (i + 1) * fa_regex.states_count

                # apply constraints
                fronts[sym][start:end] = (
                    regex_transposed_matrices[sym] @ fronts[sym][start:end]
                )

        # combine
        global_front = reduce(lambda x, y: x + y, fronts.values(), global_front)
        # remove visited states
        global_front = global_front > visited
        visited += global_front

    # fill pairs
    for regex_final_state_i in fa_regex.final_states_is:
        for i in range(len(fa_graph.start_states_is)):
            graph_start_state_i = fa_graph.start_states_is[i]
            graph_start_state: int = fa_graph.states[graph_start_state_i]._value
            # iterate over reached graph final states
            for graph_reached_state in visited.getrow(
                fa_regex.states_count * i + regex_final_state_i
            ).indices:
                if graph_reached_state not in fa_graph.final_states_is:
                    continue
                pairs.add(
                    (graph_start_state, fa_graph.states[graph_reached_state].value)
                )

    return pairs
