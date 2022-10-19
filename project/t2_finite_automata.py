from typing import List
from pyformlang.finite_automaton import (
    State,
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex
import networkx as nx
import pyformlang.finite_automaton as pfl


def build_minimal_dfa_from_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """Build minimal DFA from regular expression

    :param regex: PythonRegex
        Regular expression, which will be used for building DFA

    :return dfa: DeterministicFiniteAutomaton
        Minimal deterministic FA
    """
    return regex.to_epsilon_nfa().minimize()


def build_nfa_from_graph(
    graph: nx.MultiDiGraph,
    start_states: List[int] = None,
    final_states: List[int] = None,
) -> NondeterministicFiniteAutomaton:
    """Build NFA from networkx MultiDiGraph

    :param start_states: list of string
        List of start states. If empty, all states are start.

    :param final_states: list of string
        List of final states. If empty, all states are final.

    :param graph: networkx.MultiDiGraph

    :return nfa: NondeterministicFiniteAutomaton
    """
    if start_states is None:
        start_states = graph.nodes
    if final_states is None:
        final_states = graph.nodes
    fa = pfl.FiniteAutomaton.from_networkx(graph)
    for i in start_states:
        fa.add_start_state(State(i))
    for i in final_states:
        fa.add_final_state(State(i))
    return fa
