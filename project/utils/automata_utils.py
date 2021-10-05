from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex, MisformedRegexError
from networkx import MultiDiGraph


class AutomataException(Exception):
    """
    Base exception for automata utils
    """

    def __init__(self, msg):
        self.msg = msg


def transform_regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Transform regular expression into DFA

    Parameters
    ----------
    regex_str: str
        Regular expression represented as string
        https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        Minimal DFA built on given regular expression

    Raises
    ------
    AutomataException
        If the incorrect regular expression is passed to the function
    """

    try:
        regex = Regex(regex_str)
    except MisformedRegexError as exc:
        raise AutomataException(f"Invalid regular expression") from exc

    enfa = regex.to_epsilon_nfa()

    return enfa.minimize()


def transform_graph_to_nfa(
    graph: MultiDiGraph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    """
    Transforms graph with a given name into NFA

    Parameters
    ----------
    graph: MultiDiGraph
        Graph to transform to NFA
    start_states: set, default=None
        Start states in NFA
        If None, then every node in NFA is start
    final_states: set, default=None
        Final states in NFA
        If None, then every node in NFA is final

    Returns
    -------
    nfa: NondeterministicFiniteAutomaton
        NFA built on given graph

    Raises
    ------
    AutomataException
        If given start or final states do not match graph nodes
    """

    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    graph_nodes = graph.nodes()

    if not start_states:
        start_states = set(graph_nodes)
    if not final_states:
        final_states = set(graph_nodes)

    # Check whether start and final states are correct graph nodes
    if not start_states.issubset(graph_nodes):
        raise AutomataException(
            f"Invalid start states: {start_states.difference(set(graph_nodes))}"
        )
    if not final_states.issubset(graph_nodes):
        raise AutomataException(
            f"Invalid final states: {final_states.difference(set(graph_nodes))}"
        )

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa
