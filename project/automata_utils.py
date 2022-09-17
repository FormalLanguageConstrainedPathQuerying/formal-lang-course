from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)


def create_min_dfa_by_regex(regex) -> DeterministicFiniteAutomaton:
    """
    Creates a min DFA based on a regular expression.
    :param regex: PythonRegex
    :return: DeterministicFiniteAutomaton
    """
    return regex.to_epsilon_nfa().minimize()


def create_nfa_by_graph(graph, start_nodes=None, final_nodes=None):
    """
    Creates a NFA based on a graph.
    :param graph: MultiDiGraph
    :param final_nodes: set(Symbol)
    :param start_nodes: set(Symbol)
    :return: NondeterministicFiniteAutomaton
    """
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if start_nodes is not None:
        for node in start_nodes:
            nfa.add_start_state(node)
    else:
        for node in graph.nodes:
            nfa.add_start_state(node)
    if final_nodes is not None:
        for node in final_nodes:
            nfa.add_final_state(node)
    else:
        for node in graph.nodes:
            nfa.add_final_state(node)
    return nfa
