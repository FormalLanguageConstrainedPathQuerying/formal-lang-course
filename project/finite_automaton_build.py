import pyformlang.finite_automaton as fa
import pyformlang.regular_expression as re
import networkx as nx


def get_min_dfa(expr: re.Regex) -> fa.DeterministicFiniteAutomaton:
    """Build a minimal DFA that matches the given regular expression
    Parameters:
    reg (Regex) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    dfa = expr.to_epsilon_nfa()
    return dfa.minimize()


def get_min_dfa_from_str(expr: str) -> fa.DeterministicFiniteAutomaton:
    """Build a minimal DFA that matches the given regular expression
    Parameters:
    reg (str) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    return get_min_dfa(re.Regex(expr))


"""
def get_nfa (graph: nx.MultiDiGraph, start_states, final_states)\
        -> fa.NondeterministicFiniteAutomaton:

"""
