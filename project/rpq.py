from typing import Set, Optional, Tuple, Any

from networkx import MultiDiGraph
from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex

from project import graph_to_epsilon_nfa, BoolMatrixAutomaton, regex_to_min_dfa

__all__ = [
    "rpq",
]


def rpq(
    graph: MultiDiGraph,
    query: Regex,
    start_states: Optional[Set],
    final_states: Optional[Set],
) -> Set[Tuple[Any, Any]]:
    """Executes regular query on graph

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
