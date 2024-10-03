import scipy.sparse as sp
from scipy.sparse._csr import csr_matrix
from networkx import MultiDiGraph
from functools import reduce
from collections import defaultdict


from project.task2 import regex_to_dfa, graph_to_nfa
from project.task3 import AdjacencyMatrixFA


def get_init_front(
    adj_regex: AdjacencyMatrixFA, adj_graph: AdjacencyMatrixFA
) -> sp.csr_matrix:
    matrixes = []
    for start_state_graph in adj_graph.start_states:
        matrix = sp.lil_matrix((adj_regex.state_count, adj_graph.state_count))
        for start_state_regex in adj_regex.start_states:
            matrix[
                adj_regex.index_of_states[start_state_regex],
                adj_graph.index_of_states[start_state_graph],
            ] = 1
        matrixes.append(matrix)

    return sp.vstack(matrixes, format="csr")


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    adj_regex = AdjacencyMatrixFA(regex_to_dfa(regex))
    adj_graph = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    regex_state_count = adj_regex.state_count

    transitions = set(
        adj_regex.adjacency_matrixes_boolean_decomposition.keys()
    ).intersection(adj_graph.adjacency_matrixes_boolean_decomposition.keys())

    front = get_init_front(
        adj_regex,
        adj_graph,
    )
    visited = front

    while front.count_nonzero() > 0:
        visited += front
        fronts = defaultdict(lambda: csr_matrix(front.shape, dtype=bool))
        for transition in transitions:
            new_front = (
                front * adj_graph.adjacency_matrixes_boolean_decomposition[transition]
            )
            for start_state_num in range(len(adj_graph.start_states)):
                rows, columns = adj_regex.adjacency_matrixes_boolean_decomposition[
                    transition
                ].nonzero()
                offset = start_state_num * regex_state_count
                for row_id, column_id in zip(rows, columns):
                    fronts[transition][offset + column_id, :] += new_front[
                        offset + row_id, :
                    ]

        front = reduce(
            lambda x, y: x + y, fronts.values(), csr_matrix(front.shape, dtype=bool)
        )
        front = front > visited

    res = set()
    for final_state_index_regex in list(
        map(lambda s: adj_regex.index_of_states[s], adj_regex.final_states)
    ):
        for start_state_index, start_state_graph in enumerate(adj_graph.start_states):
            visited_slice = visited[
                regex_state_count * start_state_index : regex_state_count
                * (start_state_index + 1)
            ]
            row = visited_slice.getrow(final_state_index_regex).toarray()[0]
            index_of_final_states_graph = row.nonzero()[0]
            for index_of_final_state_graph in index_of_final_states_graph:
                final_state_graph = adj_graph.state_of_indexes[
                    index_of_final_state_graph
                ]
                if final_state_graph in adj_graph.final_states:
                    res.add(
                        (
                            start_state_graph,
                            final_state_graph,
                        )
                    )

    return res
