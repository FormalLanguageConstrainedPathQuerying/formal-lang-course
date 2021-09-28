from typing import Set, Tuple

import networkx as nx

from project.automaton_tools import get_min_dfa_from_regex, get_nfa_from_graph
from project.matrix_tools import BooleanAdjacencies

__all__ = ["regular_path_querying"]


def regular_path_querying(graph: nx.MultiDiGraph, regex: str, start_node_nums: Set[int] = None,
                          final_node_nums: Set[int] = None) -> Set[Tuple[int, int]]:
    graph = BooleanAdjacencies(get_nfa_from_graph(graph, start_node_nums, final_node_nums))
    query = BooleanAdjacencies(get_min_dfa_from_regex(regex))

    intersection = graph.intersect(query)
    transitive_closure = intersection.get_transitive_closure()

    reachable_state_nums = set()

    for state_from_num, state_to_num in zip(*transitive_closure.nonzero()):
        state_from = intersection.nums_states[state_from_num]
        state_to = intersection.nums_states[state_to_num]

        if state_from in intersection.start_states and state_to in intersection.final_states:
            reachable_state_from_num = state_from_num // query.states_num
            reachable_state_to_num = state_to_num // query.states_num

            reachable_state_nums.add((reachable_state_from_num, reachable_state_to_num))

    return reachable_state_nums
