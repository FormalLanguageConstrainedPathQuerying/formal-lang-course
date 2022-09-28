from project import BoolDecomposedNFA
import networkx as nx
from project.dfa_utils import graph_to_nfa, reg_str_to_dfa

__all__ = ["regular_path_querying"]


def regular_path_querying(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
) -> set:
    graph_bm = BoolDecomposedNFA(graph_to_nfa(graph, start_states, final_states))
    reg_bm = BoolDecomposedNFA(reg_str_to_dfa(reg_str))

    intersected_bm = graph_bm.intersect(reg_bm)

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
