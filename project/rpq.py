import enum
from typing import Set, Optional, Tuple, Any, Dict

from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project import graph_to_epsilon_nfa, BoolMatrixAutomaton, regex_to_min_dfa

__all__ = [
    "rpq_tensor",
    "rpq_bfs",
    "MultipleSourceRpqMode",
]


def rpq_tensor(
    graph: MultiDiGraph,
    query: Regex,
    start_states: Optional[Set],
    final_states: Optional[Set],
) -> Set[Tuple[Any, Any]]:
    """Executes regular query on graph using tensor multiplication

    Parameters
    ----------
    graph : MultiDiGraph
        The graph on which query will be executed
    query: Regex
        Query represented by regular expression
    start_states: Optional[Set]
        Set of nodes of the graph that will be treated as start states in NFA
        If parameter is None then each graph node is considered the start state
    final_states: Optional[Set]
        Set of nodes of the graph that will be treated as final states in NFA
        If parameter is None then each graph node is considered the final state

    Returns
    -------
    result : Set[Tuple[Any, Any]]
        The set of pairs where the node in second place is reachable
         from the node in first place with a constraint on a given query
    """
    nfa_bool_mtx = BoolMatrixAutomaton.from_nfa(
        graph_to_epsilon_nfa(
            graph=graph,
            start_states=start_states,
            final_states=final_states,
        )
    )
    query_bool_mtx = BoolMatrixAutomaton.from_nfa(
        regex_to_min_dfa(regex=query),
    )
    intersection_bool_mtx = nfa_bool_mtx & query_bool_mtx
    idx_to_state = {
        idx: state for state, idx in intersection_bool_mtx.state_to_idx.items()
    }
    transitive_closure = intersection_bool_mtx.transitive_closure()
    result = set()
    for state_from_idx, state_to_idx in zip(*transitive_closure.nonzero()):
        state_from, state_to = idx_to_state[state_from_idx], idx_to_state[state_to_idx]
        if (
            state_from in intersection_bool_mtx.start_states
            and state_to in intersection_bool_mtx.final_states
        ):
            state_from_graph_value, _ = state_from.value
            state_to_graph_value, _ = state_to.value
            result.add(
                (state_from_graph_value, state_to_graph_value),
            )
    return result


class MultipleSourceRpqMode(enum.Enum):
    """Class represents mode of multiple source rpq task

    Values
    ----------

    FIND_ALL_REACHABLE : MultipleSourceRpqMode
        Find all reachable nodes from set of start nodes
    FIND_REACHABLE_FOR_EACH_START_NODE : MultipleSourceRpqMode
        Find reachable nodes for each start node separately
    """

    FIND_ALL_REACHABLE = enum.auto()
    FIND_REACHABLE_FOR_EACH_START_NODE = enum.auto()


def rpq_bfs(
    graph: MultiDiGraph,
    query: Regex,
    start_states: Optional[Set],
    final_states: Optional[Set],
    mode: MultipleSourceRpqMode,
) -> Set[Any]:
    """Executes regular query on graph using multiple source bfs

    Parameters
    ----------
    graph : MultiDiGraph
        The graph on which query will be executed
    query: Regex
        Query represented by regular expression
    start_states: Optional[Set]
        Set of nodes of the graph that will be treated as start states in NFA
        If parameter is None then each graph node is considered the start state
    final_states: Optional[Set]
        Set of nodes of the graph that will be treated as final states in NFA
        If parameter is None then each graph node is considered the final state
    mode: MultipleSourceRpqMode
        The mode that determines which vertices should be found

    Returns
    -------
    result : Set[Any]
        Result depends on chosen mode
        if mode is FIND_ALL_REACHABLE -- set of reachable nodes
        if mode is FIND_REACHABLE_FOR_EACH_START_NODE -- set of tuples (U, V)
        where U is start node and V is final node reachable from U
    """
    nfa_bool_mtx = BoolMatrixAutomaton.from_nfa(
        graph_to_epsilon_nfa(
            graph=graph,
            start_states=start_states,
            final_states=final_states,
        )
    )
    query_bool_mtx = BoolMatrixAutomaton.from_nfa(
        regex_to_min_dfa(regex=query),
    )
    return nfa_bool_mtx.sync_bfs(
        other=query_bool_mtx,
        reachable_per_node=mode
        == MultipleSourceRpqMode.FIND_REACHABLE_FOR_EACH_START_NODE,
    )
