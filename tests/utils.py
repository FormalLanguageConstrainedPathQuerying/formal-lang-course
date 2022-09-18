from networkx import is_isomorphic, MultiDiGraph
from networkx.algorithms.isomorphism import (
    categorical_node_match,
    categorical_multiedge_match,
)


def check_graphs_are_isomorphic(first_graph, second_graph):
    return is_isomorphic(
        G1=first_graph,
        G2=second_graph,
        node_match=categorical_node_match(
            ["label", "is_start", "is_final"], [None, None, None]
        ),
        edge_match=categorical_multiedge_match("label", None),
    )


def check_automatons_are_equivalent(first_automaton, second_automaton):
    return check_graphs_are_isomorphic(
        first_graph=automaton_to_graph(first_automaton),
        second_graph=automaton_to_graph(second_automaton),
    )


def automaton_to_graph(automaton):
    graph = MultiDiGraph()
    for state_from, symbol, state_to in automaton:
        graph.add_edge(
            u_for_edge=state_from,
            v_for_edge=state_to,
            label=symbol.value,
        )
    for node, data in graph.nodes(data=True):
        data["is_start"] = node in automaton.start_states
        data["is_final"] = node in automaton.final_states
    return graph
