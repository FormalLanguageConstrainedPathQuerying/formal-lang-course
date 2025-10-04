from project import t2_fa_utils as t2
from project import t3_graph_fa as t3
from networkx import MultiDiGraph
import sparse as sp

def ms_bfs_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]) -> set[tuple[int, int]]:
    reg_dfa = t2.regex_to_dfa(regex)
    graph_nfa = t2.graph_to_nfa(graph)

    reg_am = t3.AdjacencyMatrixFA(reg_dfa)
    graph_am = t3.AdjacencyMatrixFA(graph_nfa)

    kron_matrices = {}
    for symb in reg_am.matrices.keys():
        if symb in graph_am.matrices:
            kron_matrices[symb] = sp.kron(reg_am.transitions[symb], graph_am.transitions[symb], format="csc")

    start_states = [
        (reg_dfa.state_indices[q1], graph_nfa.state_indices[q2])
        for q1 in reg_dfa.start_states
        for q2 in start_nodes
    ]

    n = reg_am.n_states * graph_am.n_states
    frontier = sp.csc_matrix((n, 1), dtype=bool)
    for (i, j) in start_states:
        frontier[i * graph_am.n_states + j, 0] = True

    visited = frontier.copy()
    changed = True
    while changed:
        next_frontier = sp.csc_matrix((n, 1), dtype=bool)
        for m in kron_matrices.values():
            print(m)
            # for each sym of reg_am -> get all the transitions with sym m and unite them
            next_frontier += m @ frontier
        next_frontier.data[:] = True # remove the duplicates by transfering the data to bool
        new = next_frontier.multiply(~visited) # remove already visited nodes
        changed = new.nnz > 0 # if after multiply we got zeros -> we had loops
        visited += new
        frontier = new
        print(frontier)

    result = set()
    for q_reg_idx in reg_dfa.final_states:
        for q_graph_idx in final_nodes:
            idx = q_reg_idx * graph_am.n_states + q_graph_idx
            if visited[idx, 0]:
                result.add((q_reg_idx, q_graph_idx))

    return result
