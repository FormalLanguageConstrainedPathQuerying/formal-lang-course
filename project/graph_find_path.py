import networkx as nx
from project.boolean_matrices import (
    cross_boolean_matrices,
    nfa_to_boolean_matrices,
    transitive_closure,
)
from project.dfa_utils import graph_to_nfa, regex_str_to_dfa


def graph_find_path(
    graph: nx.MultiDiGraph,
    reg_str: str,
    start_states: set = None,
    final_states: set = None,
) -> set:
    graph_bm = nfa_to_boolean_matrices(graph_to_nfa(graph, start_states, final_states))
    reg_bm = nfa_to_boolean_matrices(regex_str_to_dfa(reg_str))

    cross = cross_boolean_matrices(graph_bm, reg_bm)

    if len(cross.matrices) == 0:
        return set()

    tc = transitive_closure(cross)

    res = set()
    for start, final in zip(*tc.nonzero()):
        if (
            cross.start_vector.toarray()[0, start]
            and cross.final_vector.toarray()[0, final]
        ):
            res.add((start // reg_bm.states_count, final // reg_bm.states_count))

    return res
