import pyformlang.finite_automaton as fa
import pyformlang.regular_expression as re
import networkx as nx


def get_min_dfa_from_regex(expr: re.Regex) -> fa.DeterministicFiniteAutomaton:
    """Build a minimal DFA that matches the given regular expression
    Parameters:
    reg (Regex) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    dfa = expr.to_epsilon_nfa()
    return dfa.minimize()


def get_min_dfa_from_regex_str(expr: str) -> fa.DeterministicFiniteAutomaton:
    """Build a minimal DFA that matches the given regular expression
    Parameters:
    reg (str) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    return get_min_dfa_from_regex(re.Regex(expr))


def get_nfa_from_graph(
    graph: nx.MultiDiGraph, start_states=None, final_states=None
) -> fa.NondeterministicFiniteAutomaton:
    """
    :param graph:
    :param start_states:
    :param final_states:
    :return:
    """
    nfa = fa.NondeterministicFiniteAutomaton.from_networkx(graph)
    nodes = graph.nodes()
    if start_states is None:
        for node in nodes:
            nfa.add_start_state(node)
    else:
        for state in start_states:
            nfa.add_start_state(state)
    if final_states is None:
        for node in nodes:
            nfa.add_final_state(node)
    else:
        for state in final_states:
            nfa.add_final_state(state)
    return nfa
