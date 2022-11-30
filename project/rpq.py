import networkx as nx
from pyformlang.regular_expression import Regex

from project.boolean_decompositonNFA import (
    BooleanDecompositionNFA,
)
from project.regex_utils import create_nfa_from_graph, regex_to_dfa


def rpq(
    graph: nx.MultiDiGraph, query: str, start_nodes: set = None, final_nodes: set = None
) -> set:
    nfa = create_nfa_from_graph(graph, start_nodes, final_nodes)
    dfa = regex_to_dfa(Regex(query))

    nfa_decomposition = BooleanDecompositionNFA(nfa)
    query_decomposition = BooleanDecompositionNFA(dfa)

    intersected = nfa_decomposition.get_intersect_boolean_decomposition(
        query_decomposition
    )
    transitive_closure = intersected.make_transitive_closure()

    start_states = intersected.get_start_states()
    final_states = intersected.get_final_states()

    rpq = set()
    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            rpq.add(
                (
                    state_from // query_decomposition.states_num,
                    state_to // query_decomposition.states_num,
                )
            )

    return rpq
