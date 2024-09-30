from scipy.sparse import (
    csr_matrix,
    vstack,
)
from project.finite_automata_lib import regex_to_dfa, graph_to_nfa
from networkx import MultiDiGraph
from project.adjacency_matrix_fa import AdjacencyMatrixFA
from typing import Set
from pyformlang.finite_automaton import State


def init_frontier(reg_mat, graph_mat, start_states_id) -> csr_matrix:
    n = graph_mat.states_count
    k = reg_mat.states_count
    frontier_row = csr_matrix((1, n), dtype=bool)

    for i in start_states_id:
        frontier_row[0, i] = True
    frontier = csr_matrix((k, n), dtype=bool)

    for i in reg_mat.start_states_id:
        frontier[i, :] = frontier_row
    return frontier


def multiple_source_bfs(graph_mat, reg_mat) -> set[tuple[int, int]]:
    if len(graph_mat.start_states_id) == 0:
        return set()

    new_symbols = (
        graph_mat.bool_decomposition.keys() & reg_mat.bool_decomposition.keys()
    )

    """ MS BFS"""
    frontier = vstack(
        [
            init_frontier(reg_mat, graph_mat, {start_vertex})
            for start_vertex in graph_mat.start_states_id
        ]
    )
    is_visited = frontier

    while True:
        new_frontier = csr_matrix(frontier.shape, dtype=bool)

        for symbol in new_symbols:
            new_frontier_component = frontier.dot(graph_mat.bool_decomposition[symbol])

            for start_start_id in range(len(graph_mat.start_states_id)):
                coressponding_frontier_position = start_start_id * reg_mat.states_count
                rows, cols = reg_mat.bool_decomposition[symbol].nonzero()

                for row, col in zip(rows, cols):
                    new_frontier[coressponding_frontier_position + col, :] += (
                        new_frontier_component[coressponding_frontier_position + row, :]
                    )

        frontier = new_frontier > is_visited

        if frontier.count_nonzero() == 0:
            break

        is_visited += frontier

    def reachable_vertices(start_node_id: int) -> Set[State]:
        coressponding_frontier_position = start_node_id * reg_mat.states_count
        reachable_states = csr_matrix((1, graph_mat.states_count), dtype=bool)

        for final_state in reg_mat.final_states_id:
            reachable_states += is_visited[
                coressponding_frontier_position + final_state, :
            ]

        reachable_vertex_id = reachable_states.nonzero()[1]
        return {
            graph_mat.id_state[i]
            for i in reachable_vertex_id
            if i in graph_mat.final_states_id
        }

    return {
        (graph_mat.id_state[start_state_id], reachable_state)
        for frontier_number, start_state_id in enumerate(graph_mat.start_states_id)
        for reachable_state in reachable_vertices(frontier_number)
    }


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    reg_mat = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_mat = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_states=start_nodes, final_states=final_nodes)
    )
    return multiple_source_bfs(graph_mat, reg_mat)
