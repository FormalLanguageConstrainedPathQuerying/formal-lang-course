from project import CBBoolDecomposedNFA
from project.dfa_utils import graph_to_nfa, reg_str_to_dfa
import networkx as nx
import pycubool as cb

__all__ = [
    "cb_rpq_by_bm",
    "cb_rpq_by_reg_str",
    "cb_rpq_by_bm_from_start",
    "cb_rpq_by_reg_str_from_start",
]


def block_diag(m1: cb.Matrix, m1_size: int, m2: cb.Matrix, m2_size: int) -> cb.Matrix:
    m3_size = m1_size + m2_size
    m3 = cb.Matrix.empty(shape=(m3_size, m3_size))
    for x, y in m1.to_list():
        m3[x, y] = True
    for x, y in m2.to_list():
        x += m1_size
        y += m1_size
        m3[x, y] = True
    return m3


def cb_rpq_by_bm_from_start(
    graph: nx.MultiDiGraph,
    bm: CBBoolDecomposedNFA,
    start_states: set = None,
    final_states: set = None,
    separated: bool = False,
) -> set:
    graph_bm = CBBoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    if graph_bm.take_states_count() == 0:
        return set()
    graph_start_states = graph_bm.take_start_vector()
    start_states = graph_start_states.to_lists()[1]
    final_states = set(graph_bm.take_final_vector().to_lists()[1])
    start_states_count = graph_start_states.nvals
    graph_states_count = graph_bm.take_states_count()
    graph_dict = graph_bm.take_dict()
    graph_bm = graph_bm.take_matrices()

    reg_bm = bm
    if reg_bm.take_states_count() == 0:
        return set()
    reg_start_states = reg_bm.take_start_vector()
    reg_final_states = reg_bm.take_final_vector()
    reg_states_count = reg_bm.take_states_count()
    reg_bm = reg_bm.take_matrices()

    std_matrix_shape = None
    if not separated:
        std_matrix_shape = (reg_states_count, graph_states_count + reg_states_count)
    else:
        std_matrix_shape = (
            reg_states_count * start_states_count,
            graph_states_count + reg_states_count,
        )

    intersecting_labels = graph_bm.keys() & reg_bm.keys()
    block_bm = {}
    for i in intersecting_labels:
        block_bm[i] = block_diag(
            reg_bm[i], reg_states_count, graph_bm[i], graph_states_count
        )

    curr_state = cb.Matrix.empty(shape=std_matrix_shape)
    mask = curr_state.dup()

    if not separated:
        for i in reg_start_states.to_lists()[1]:
            curr_state[i, i] = True
            for j in graph_start_states.to_lists()[1]:
                curr_state[i, j + reg_states_count] = True
    else:
        for j in range(0, start_states_count):
            for i in reg_start_states.to_lists()[1]:
                x = reg_states_count * j + i
                curr_state[x, i] = True
                curr_state[x, reg_states_count + start_states[j]] = True

    prev_nnz = None
    curr_nnz = mask.nvals
    while prev_nnz != curr_nnz:
        new_state = cb.Matrix.empty(shape=std_matrix_shape)
        for m in block_bm.values():
            m_state = curr_state.mxm(m)
            m_state_reg = m_state[0:, 0:reg_states_count]
            m_state_graph = m_state[0:, reg_states_count:]
            for x, y in m_state_reg.to_list():
                x_ns = reg_states_count * (x // reg_states_count) + y
                new_state[x_ns, y % reg_states_count] = True
                new_row = new_state[x_ns : x_ns + 1, reg_states_count:].ewiseadd(
                    m_state_graph[x : x + 1, 0:]
                )
                for i in new_row.to_lists()[1]:
                    new_state[x_ns, i + reg_states_count] = True
        curr_state = new_state
        mask = mask.ewiseadd(curr_state)
        prev_nnz = curr_nnz
        curr_nnz = mask.nvals

    res = None

    mask_set = set(mask.to_list())

    if not separated:
        res = cb.Matrix.empty(shape=(1, graph_states_count))
        for i in reg_final_states.to_lists()[1]:
            if (i, i) in mask:
                res = res.ewiseadd(mask[i : i + 1, reg_states_count:])
    else:
        res = cb.Matrix.empty(shape=(start_states_count, graph_states_count))
        for j in range(0, start_states_count):
            for i in reg_final_states.to_lists()[1]:
                x = reg_states_count * j + i
                if (x, i) in mask:
                    new_row = res[j : j + 1, 0:].ewiseadd(
                        mask[x : x + 1, reg_states_count:]
                    )
                    for r in new_row.to_lists()[1]:
                        res[j, r] = True

    if not separated:
        res = {graph_dict[i] for i in res.to_lists()[1] if i in final_states}
    else:
        res = {
            (graph_dict[start_states[s]], graph_dict[f])
            for s, f in res.to_list()
            if f in final_states
        }

    return res


def cb_rpq_by_reg_str_from_start(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
    separated: bool = False,
) -> set:
    return cb_rpq_by_bm_from_start(
        graph,
        CBBoolDecomposedNFA(reg_str_to_dfa(reg_str)),
        start_states,
        final_states,
        separated,
    )


def cb_rpq_by_bm(
    graph: nx.MultiDiGraph,
    bm: CBBoolDecomposedNFA,
    start_states: set = None,
    final_states: set = None,
) -> set:
    graph_bm = CBBoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    reg_bm = bm

    intersected_bm = graph_bm & reg_bm

    tc = intersected_bm.transitive_closure()

    if tc is None:
        return set()

    start_vector_array = set(intersected_bm.get_start_vector().to_list())
    final_vector_array = set(intersected_bm.get_final_vector().to_list())

    res = set()
    for start, final in tc.to_list():
        if (0, start) in start_vector_array and (0, final) in final_vector_array:
            res.add(
                (
                    graph_bm.take_dict()[start // reg_bm.get_states_count()],
                    graph_bm.take_dict()[final // reg_bm.get_states_count()],
                )
            )

    return res


def cb_rpq_by_reg_str(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
) -> set:
    return cb_rpq_by_bm(
        graph, CBBoolDecomposedNFA(reg_str_to_dfa(reg_str)), start_states, final_states
    )
