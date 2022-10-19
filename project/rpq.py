from project import BoolDecomposedNFA
from project.dfa_utils import graph_to_nfa, reg_str_to_dfa
import networkx as nx
from scipy import sparse
from scipy.sparse import dok_matrix

__all__ = [
    "rpq",
    "rpq_reg_str",
    "rpq_bfs",
    "rpq_bfs_reg_str",
]


def rpq_bfs(
    graph: nx.MultiDiGraph,
    bm: BoolDecomposedNFA,
    start_states: set = None,
    final_states: set = None,
    separated: bool = False,
) -> set:
    graph_bm = BoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    graph_start_states = graph_bm.take_start_vector()
    start_states = graph_start_states.nonzero()[1]
    final_states = set(graph_bm.take_final_vector().nonzero()[1])
    graph_states_count = graph_bm.take_states_count()
    graph_dict = graph_bm.take_dict()
    graph_bm = graph_bm.take_matrices()

    reg_bm = bm
    reg_start_states = reg_bm.take_start_vector()
    reg_final_states = reg_bm.take_final_vector()
    reg_states_count = reg_bm.take_states_count()
    reg_bm = reg_bm.take_matrices()

    shape = (reg_states_count, graph_states_count + reg_states_count)

    intersecting_labels = graph_bm.keys() & reg_bm.keys()
    block_bm = {}
    for i in intersecting_labels:
        block_bm[i] = sparse.block_diag((reg_bm[i], graph_bm[i]))

    curr_state = dict()
    mask = dict()
    queue = []

    if not separated:
        curr_state[0] = dok_matrix(shape, dtype=bool)
        for i in reg_start_states.nonzero()[1]:
            curr_state[0][i, i] = True
            curr_state[0][i, reg_states_count:] = graph_start_states
        queue.append(0)
    else:
        for s in start_states:
            curr_state[s] = dok_matrix(shape, dtype=bool)
            for i in reg_start_states.nonzero()[1]:
                curr_state[s][i, i] = True
                curr_state[s][i, reg_states_count + s] = True
            queue.append(s)

    mask = {i: m.copy() for i, m in curr_state.items()}

    curr_nnz = {i: m.nnz for i, m in mask.items()}
    while queue != []:
        for s in queue:
            new_state = dok_matrix(shape, dtype=bool)
            for m in block_bm.values():
                m_state = curr_state[s] * m
                m_state_reg = m_state[0:, 0:reg_states_count]
                m_state_graph = m_state[0:, reg_states_count:]
                for x, y in zip(*m_state_reg.nonzero()):
                    new_state[y, y] = True
                    new_state[y, reg_states_count:] += m_state_graph[x]
            curr_state[s] = new_state
            mask[s] = mask[s] + new_state
        prev_nnz = curr_nnz
        curr_nnz = {i: m.nnz for i, m in mask.items()}
        queue = [s for s in queue if prev_nnz[s] != curr_nnz[s]]

    res = None
    if not separated:
        res = dok_matrix((1, graph_states_count), dtype=bool)
        for i in reg_final_states.nonzero()[1]:
            if mask[0][i, i]:
                res += mask[0][i, reg_states_count:]
        res = {graph_dict[i] for i in res.nonzero()[1] if i in final_states}
    else:
        res = set()
        for s in start_states:
            pre_res = dok_matrix((1, graph_states_count), dtype=bool)
            for i in reg_final_states.nonzero()[1]:
                if mask[s][i, i]:
                    pre_res += mask[s][i, reg_states_count:]
            for f in pre_res.nonzero()[1]:
                if f in final_states:
                    res.add((graph_dict[s], graph_dict[f]))

    return res


def rpq_bfs_reg_str(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
    separated: bool = False,
) -> set:
    return rpq_bfs(
        graph,
        BoolDecomposedNFA(reg_str_to_dfa(reg_str)),
        start_states,
        final_states,
        separated,
    )


def rpq(
    graph: nx.MultiDiGraph,
    bm: BoolDecomposedNFA,
    start_states: set = None,
    final_states: set = None,
) -> set:
    graph_bm = BoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    reg_bm = bm

    intersected_bm = graph_bm & reg_bm

    tc = intersected_bm.transitive_closure()

    start_vector_array = intersected_bm.get_start_vector().toarray()
    final_vector_array = intersected_bm.get_final_vector().toarray()

    res = set()
    for start, final in zip(*tc.nonzero()):
        if start_vector_array[0, start] and final_vector_array[0, final]:
            res.add(
                (
                    graph_bm.take_dict()[start // reg_bm.get_states_count()],
                    graph_bm.take_dict()[final // reg_bm.get_states_count()],
                )
            )

    return res


def rpq_reg_str(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
) -> set:
    return rpq(
        graph, BoolDecomposedNFA(reg_str_to_dfa(reg_str)), start_states, final_states
    )
