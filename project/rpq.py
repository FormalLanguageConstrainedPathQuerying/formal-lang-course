from typing import Set, Tuple

from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.automata_tools import graph_to_nfa, regex_to_minimal_dfa
from project.boolean_matrices import BooleanMatrices

from project.automata_tools import create_nfa_from_graph


def rpq(graph: MultiDiGraph, query: Regex, start_nodes: set, final_nodes: set):
    nfa = create_nfa_from_graph(graph, start_nodes, final_nodes)
    graph_bm = BooleanMatrices.from_automaton(nfa)
    query_bm = BooleanMatrices.from_automaton(regex_to_minimal_dfa(query))
    intersection_bm = graph_bm.intersect(query_bm)
    return get_reachable(intersection_bm, query_bm)


def get_reachable(
    b_matrix: BooleanMatrices, query_bm: BooleanMatrices = None
) -> Set[Tuple[int, int]]:

    transitive_closure = b_matrix.transitive_closure()

    start_states = b_matrix.get_start_states()
    final_states = b_matrix.get_final_states()

    result_set = set()

    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result_set.add(
                (
                    state_from // query_bm.num_states
                    if query_bm is not None
                    else b_matrix.num_states,
                    state_to // query_bm.num_states
                    if query_bm is not None
                    else b_matrix.num_states,
                )
            )

    return result_set
