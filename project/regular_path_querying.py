from project import BoolDecomposedNFA
from project.dfa_utils import graph_to_nfa, reg_str_to_dfa
import networkx as nx
from scipy import sparse
from scipy.sparse import dok_matrix

__all__ = ["regular_path_querying", "regular_path_querying_from_start"]


def regular_path_querying_from_start(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    separately_for_each: bool = False,
) -> set:
    graph_bm = BoolDecomposedNFA(graph_to_nfa(graph, start_states))
    graph_start_states = graph_bm.take_start_vector()
    start_states = graph_start_states.nonzero()[1]
    start_states_count = graph_start_states.nnz
    graph_states_count = graph_bm.take_states_count()
    graph_bm = graph_bm.take_matrices()

    reg_bm = BoolDecomposedNFA(reg_str_to_dfa(reg_str))
    reg_start_states = reg_bm.take_start_vector()
    reg_final_states = reg_bm.take_final_vector()
    reg_states_count = reg_bm.take_states_count()
    reg_bm = reg_bm.take_matrices()

    std_matrix_shape = None
    if not separately_for_each:
        std_matrix_shape = (reg_states_count, graph_states_count + reg_states_count)
    else:
        std_matrix_shape = (
            reg_states_count * start_states_count,
            graph_states_count + reg_states_count,
        )

    intersecting_labels = graph_bm.keys() & reg_bm.keys()
    block_bm = {}
    for i in intersecting_labels:
        block_bm[i] = sparse.block_diag((reg_bm[i], graph_bm[i]))

    curr_state = dok_matrix(std_matrix_shape, dtype=bool)
    mask = curr_state.copy()

    if not separately_for_each:
        for i in reg_start_states.nonzero()[1]:
            curr_state[i, i] = True
            curr_state[i, reg_states_count:] = graph_start_states
    else:
        for j in range(0, start_states_count):
            for i in reg_start_states.nonzero()[1]:
                x = reg_states_count * j + i
                curr_state[x, i] = True
                curr_state[x, reg_states_count + start_states[j]] = True

    prev_nnz = None
    curr_nnz = mask.nnz
    while prev_nnz != curr_nnz:
        new_state = dok_matrix(std_matrix_shape, dtype=bool)
        for m in block_bm.values():
            m_state = curr_state * m
            m_state_reg = m_state[0:, 0:reg_states_count]
            m_state_graph = m_state[0:, reg_states_count:]
            for x, y in zip(*m_state_reg.nonzero()):
                x_ns = reg_states_count * (x // reg_states_count) + y
                new_state[x_ns, y % reg_states_count] = True
                new_state[x_ns, reg_states_count:] += m_state_graph[x]
        curr_state = new_state
        mask += curr_state
        prev_nnz = curr_nnz
        curr_nnz = mask.nnz

    res = None
    if not separately_for_each:
        res = dok_matrix((1, graph_states_count), dtype=bool)
        for i in reg_final_states.nonzero()[1]:
            if mask[i, i]:
                res += mask[i, reg_states_count:]
    else:
        res = dok_matrix((start_states_count, graph_states_count), dtype=bool)
        for j in range(0, start_states_count):
            for i in reg_final_states.nonzero()[1]:
                x = reg_states_count * j + i
                if mask[x, i]:
                    res[j] += mask[x, reg_states_count:]

    if not separately_for_each:
        res = set(res.nonzero()[1])
    else:
        res = {(start_states[s], f) for s, f in zip(*res.nonzero())}

    return res


def regular_path_querying(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
) -> set:
    graph_bm = BoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    reg_bm = BoolDecomposedNFA(reg_str_to_dfa(reg_str))

    intersected_bm = graph_bm & reg_bm

    tc = intersected_bm.transitive_closure()

    start_vector_array = intersected_bm.get_start_vector().toarray()
    final_vector_array = intersected_bm.get_final_vector().toarray()

    res = set()
    for start, final in zip(*tc.nonzero()):
        if start_vector_array[0, start] and final_vector_array[0, final]:
            res.add(
                (start // reg_bm.get_states_count(), final // reg_bm.get_states_count())
            )

    return res
