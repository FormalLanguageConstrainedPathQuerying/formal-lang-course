import numpy as np
from networkx import MultiDiGraph
from scipy import sparse
from project.hw2.graph_to_nfa_tool import graph_to_nfa
from project.hw2.regex_to_dfa_tool import regex_to_dfa
from project.hw3.AdjacencyMatrixFA import AdjacencyMatrixFA
from project.tools.vector_tool import create_bool_vector


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    reg_fa = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_nfa = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    fa_dim = reg_fa.states_cnt
    nfa_dim = graph_nfa.states_cnt
    dfa_start_state_index = list(reg_fa.start_states_ind)[0]
    nfa_start_states_indexes = graph_nfa.start_states_ind
    nfa_start_states_cnt = len(nfa_start_states_indexes)

    gen_labels = (
        reg_fa.boolean_decomposition.keys() & graph_nfa.boolean_decomposition.keys()
    )

    dfa_bool_decompose = reg_fa.boolean_decomposition
    transposed_matrices = {}
    for label in gen_labels:
        transposed_matrices[label] = dfa_bool_decompose[label].transpose()
    nfa_bool_decompose = graph_nfa.boolean_decomposition

    data = np.ones(nfa_start_states_cnt, dtype=bool)
    rows = [dfa_start_state_index + fa_dim * j for j in range(nfa_start_states_cnt)]
    columns = [el for el in nfa_start_states_indexes]
    cur_front = sparse.csr_matrix(
        (data, (rows, columns)),
        shape=(fa_dim * nfa_start_states_cnt, nfa_dim),
        dtype=bool,
    )
    visited = sparse.csr_matrix((fa_dim * nfa_start_states_cnt, nfa_dim), dtype=bool)

    while cur_front.count_nonzero() > 0:
        visited += cur_front
        front_bool_decompositions = {}

        for label in gen_labels:
            front_bool_decompositions[label] = cur_front @ nfa_bool_decompose[label]
            for i in range(nfa_start_states_cnt):
                front_bool_decompositions[label][i * fa_dim : (i + 1) * fa_dim] = (
                    transposed_matrices.get(label)
                    @ front_bool_decompositions[label][i * fa_dim : (i + 1) * fa_dim]
                )
        new_front = sparse.csr_matrix(
            (fa_dim * nfa_start_states_cnt, nfa_dim), dtype=bool
        )
        for front in front_bool_decompositions.values():
            new_front += front
        cur_front = new_front
        cur_front = cur_front > visited
    dfa_final_states_indexes = reg_fa.final_states_ind
    nfa_final_states_indexes = graph_nfa.final_states_ind
    nfa_final_states_vec = create_bool_vector(
        graph_nfa.states_cnt, nfa_final_states_indexes
    )

    res = set()
    for i, nfa_start_st_ind in enumerate(nfa_start_states_indexes, 0):
        for dfa_final_st_ind in dfa_final_states_indexes:
            row = visited.getrow(i * fa_dim + dfa_final_st_ind)
            row_vec = create_bool_vector(nfa_dim, row.indices)

            vec = row_vec & nfa_final_states_vec
            reached_nfa_fin_sts_ind = np.nonzero(vec)[0]
            for reached_nfa_fin_st_ind in reached_nfa_fin_sts_ind:
                res.add(
                    (
                        graph_nfa.numbered_node_labels[nfa_start_st_ind],
                        graph_nfa.numbered_node_labels[reached_nfa_fin_st_ind],
                    )
                )
    return res
