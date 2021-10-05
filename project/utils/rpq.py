from networkx import MultiDiGraph

from project.utils.matrix_utils import BooleanMatrix
from project.utils.automata_utils import transform_graph_to_nfa, transform_regex_to_dfa


def rpq(
    graph: MultiDiGraph, query: str, start_nodes: set = None, final_nodes: set = None
):
    """
    Computes Regular Path Querying from given graph language and regular expression language

    Parameters
    ----------
    graph: MultiDiGraph
       Labeled graph
    query: str
       Regular expression given as string
    start_nodes: set, default=None
       Start states in NFA
    final_nodes: set, default=None
       Final states in NFA

    Returns
    -------
    rpq: set
       Regular Path Querying
    """

    graph_bm = BooleanMatrix.from_nfa(
        transform_graph_to_nfa(graph, start_nodes, final_nodes)
    )
    query_bm = BooleanMatrix.from_nfa(transform_regex_to_dfa(query))

    intersection = graph_bm.intersect(query_bm)
    tc = intersection.transitive_closure()

    result = set()
    for state_from, state_to in zip(*tc.nonzero()):
        if (
            state_from in intersection.start_states
            and state_to in intersection.final_states
        ):
            result.add(
                (
                    state_from // len(query_bm.indexed_states),
                    state_to // len(query_bm.indexed_states),
                )
            )

    return result
