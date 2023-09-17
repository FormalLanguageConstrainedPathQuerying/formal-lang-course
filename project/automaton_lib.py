from typing import List

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph
from networkx import set_node_attributes


def dfa_of_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Creates deterministic finite automaton from regex

    Args:
        regex: Regular expression to generate DFA from

    Returns:
        Minimal deterministic finite automaton
    """
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def nfa_of_graph(
    graph: MultiDiGraph,
    starting_nodes: List[int] | None = None,
    final_nodes: List[int] | None = None,
) -> NondeterministicFiniteAutomaton:
    """
    Creates nondeterministic finite automaton from networkx MultiDiGraph

    Args:
        graph: Graph to make automaton from
        To indicate starting node, "is_start" data should be set to True
        To indicate final node, "is_final" data should be set to True
        Data "label" is needed for transition to be valid
        Starting and final nodes will be overriden if starting_nodes or
        final_nodes will be supplied respectively

        starting_nodes: List of starting nodes
        Overrides is_start from the graph given

        final_nodes: List of final nodes
        Overrides is_final from the graph given

    Returns:
        Generated nondeterministic finite automaton
    """

    graph = graph.copy()

    if starting_nodes is not None:
        set_node_attributes(
            graph, {i: i in starting_nodes for i in graph.nodes}, name="is_start"
        )

    if final_nodes is not None:
        set_node_attributes(
            graph, {i: i in final_nodes for i in graph.nodes}, name="is_final"
        )

    automaton = NondeterministicFiniteAutomaton.from_networkx(graph)

    return automaton
