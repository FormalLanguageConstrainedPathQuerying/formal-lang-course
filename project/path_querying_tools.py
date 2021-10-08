from typing import Set, Tuple

import networkx as nx
from pyformlang.regular_expression import Regex

from project.automaton_tools import get_min_dfa_from_regex, get_nfa_from_graph
from project.matrix_tools import BooleanAdjacencies

__all__ = ["regular_path_querying"]


def regular_path_querying(
    graph: nx.MultiDiGraph,
    query_str: str,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
    mode: str = "cpu",
    query_regex: Regex = None,
) -> Set[Tuple[int, int]]:
    """
    Using the specified graph and a regular query,
    finds all pairs of reachable node numbers.

    If actual regex is specified, regex_str is no longer taken into account.

    If start_nodes or final_nodes are not specified,
    all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    query_str: str
        Query to graph as a string
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    mode: str, default = "cpu"
        Allows to select the platform used for all calculations
    query_regex: Regex, default = None
        Query to graph as complete Regex

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers

    Raises
    ------
    ValueError
        If invalid computing platform specified
    ValueError
        If non-existent in the specified graph node number is used
    MisformedRegexError
        If specified regex_str has an irregular format
    """

    graph = BooleanAdjacencies(
        get_nfa_from_graph(graph, start_node_nums, final_node_nums), mode
    )

    re_query = None
    if query_regex is None:
        re_query = Regex(query_str)
    else:
        re_query = query_regex

    query = BooleanAdjacencies(get_min_dfa_from_regex(re_query), mode)

    intersection = graph.intersect(query)
    transitive_closure = intersection.get_transitive_closure()

    reachable_state_nums = set()

    if mode == "cpu":
        for state_from_num, state_to_num in zip(*transitive_closure.nonzero()):
            state_from = intersection.nums_states[state_from_num]
            state_to = intersection.nums_states[state_to_num]

            if (
                state_from in intersection.start_states
                and state_to in intersection.final_states
            ):
                reachable_state_from_num = state_from_num // query.states_num
                reachable_state_to_num = state_to_num // query.states_num

                reachable_state_nums.add(
                    (reachable_state_from_num, reachable_state_to_num)
                )

    if mode == "gpu":
        for state_from_num, state_to_num in zip(*transitive_closure.to_lists()):
            state_from = intersection.nums_states[state_from_num]
            state_to = intersection.nums_states[state_to_num]

            if (
                state_from in intersection.start_states
                and state_to in intersection.final_states
            ):
                reachable_state_from_num = state_from_num // query.states_num
                reachable_state_to_num = state_to_num // query.states_num

                reachable_state_nums.add(
                    (reachable_state_from_num, reachable_state_to_num)
                )

    return reachable_state_nums