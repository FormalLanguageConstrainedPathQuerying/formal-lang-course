import numpy as np
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from scipy.sparse import csr_matrix, SparseEfficiencyWarning, lil_matrix

from project.automata_utils import (
    from_regex_to_dfa,
    boolean_decompose_enfa,
    intersect_enfa,
)
from project.graph_utils import from_graph_to_nfa

from project.regular_path_query_bfs import regular_bfs

__all__ = ["regular_path_query", "bfs_based_regular_path_query"]


def bfs_based_regular_path_query(
    regex: Regex,
    graph: MultiDiGraph,
    separated: bool,
    start_states: list[any] = None,
    final_states: list[any] = None,
) -> set[any] | dict[any, set[any]]:
    """
    Performs rpq (regular path query) in graph with regex
    :param regex: regex to define regular path query
    :param graph: graph to be inspected
    :param separated: if true result will be presented as dictionary where key node from start_states and value is set
        of nodes which can be obtained from this node by rpq, otherwise result will be presented as set of graph nodes
        which may be obtained from start_states
    :param start_states: start nodes to rpq inside graph
    :param final_states: final nodes to rpq inside graph
    :return: if separated = True result will be presented as dictionary where key node from start_states and value is
        set of nodes which can be obtained from this node by rpq, otherwise result will be presented as set of graph
        nodes which may be obtained from start_states
    """
    result = regular_bfs(
        boolean_decompose_enfa(from_graph_to_nfa(graph)),
        regex,
        separated,
        start_states,
        final_states,
    )
    if not separated:
        return result
    else:
        divided_result = dict()
        for (i, j) in result:
            if i not in divided_result:
                divided_result[i] = set()
            divided_result[i].add(j)
        return divided_result


def regular_path_query(
    regex: Regex,
    graph: MultiDiGraph,
    start_states: list[any] = None,
    final_states: list[any] = None,
) -> set[tuple[any, any]]:
    """
    Performs rpq (regular path query) in graph with regex
    :param regex: regex to define regular path query
    :param graph: graph to be inspected
    :param start_states: start nodes to rpq inside graph
    :param final_states: final nodes to rpq inside graph
    :return: 2 element tuples with nodes satisfying rpq
    """
    if start_states is None:
        start_states = list(graph.nodes)

    if final_states is None:
        final_states = list(graph.nodes)

    graph_as_enfa = from_graph_to_nfa(graph, start_states, final_states)
    regex_as_enfa = from_regex_to_dfa(regex)
    intersection_enfa = intersect_enfa(graph_as_enfa, regex_as_enfa)

    boolean_decompose_intersection = boolean_decompose_enfa(intersection_enfa)
    intersection_states = boolean_decompose_intersection.states()
    transitive_closure_of_intersection = (
        boolean_decompose_intersection.transitive_closure()
    )
    transitive_closure_connected_states = zip(
        *transitive_closure_of_intersection.nonzero()
    )
    results = set()
    for (i, j) in transitive_closure_connected_states:
        (graph_start_state, regex_start_state) = intersection_states[i].value
        (graph_final_state, regex_final_state) = intersection_states[j].value
        if (
            graph_start_state in start_states
            and graph_final_state in final_states
            and regex_start_state in regex_as_enfa.start_states
            and regex_final_state in regex_as_enfa.final_states
        ):
            results.add((graph_start_state, graph_final_state))

    return results
