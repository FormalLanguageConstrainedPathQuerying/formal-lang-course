from networkx import MultiDiGraph
from project.task2 import regex_to_dfa, graph_to_nfa
from project.task3 import AdjacencyMatrixFA
import scipy as sp


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    regex_dfa = regex_to_dfa(regex)

    graph_adj = AdjacencyMatrixFA(graph_nfa)
    regex_adj = AdjacencyMatrixFA(regex_dfa)

    new_start_states = list()
    for i1 in regex_adj.start_states:
        for i2 in graph_adj.start_states:
            new_start_states.append((i1, i2))

    matrices = []
    for regex_adj_state, graph_adj_state in new_start_states:
        matrix = sp.sparse.csc_matrix(
            (regex_adj.number_of_states, graph_adj.number_of_states), dtype=bool
        )
        matrix[regex_adj_state, graph_adj_state] = True
        matrices.append(matrix)

    initial_front = sp.sparse.vstack(matrices, format="csc", dtype=bool)
    front = initial_front
    visited = front

    symbols = set(
        regex_adj.bool_decomposition.keys() & set(graph_adj.bool_decomposition.keys())
    )
    permutation_matr = {
        symbol: regex_adj.bool_decomposition[symbol].transpose() for symbol in symbols
    }

    while front.count_nonzero() > 0:
        symbols_fronts = []

        for symbol in symbols:
            symbol_front = front @ graph_adj.bool_decomposition[symbol]
            new_symbol_front_matr = [
                permutation_matr[symbol]
                @ symbol_front[
                    regex_adj.number_of_states * i : regex_adj.number_of_states
                    * (i + 1)
                ]
                for i in range(len(new_start_states))
            ]

            new_front = sp.sparse.vstack(
                new_symbol_front_matr, format="csc", dtype=bool
            )
            symbols_fronts.append(new_front)

        front = sum(symbols_fronts) > visited
        visited += front

    result = set()
    for regex_final in regex_adj.final_states:
        for i, graph_start in enumerate(graph_adj.start_states):
            block = visited[
                regex_adj.number_of_states * i : regex_adj.number_of_states * (i + 1)
            ]
            for graph_final in graph_adj.final_states:
                if block[regex_final, graph_final]:
                    result.add(
                        (
                            graph_adj.index_to_state[graph_start],
                            graph_adj.index_to_state[graph_final],
                        )
                    )

    return result
