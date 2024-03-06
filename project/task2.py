from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex


def regex_to_dfa(re: str) -> DeterministicFiniteAutomaton:
    """
    Converts a given regular expression into a deterministic finite automaton (DFA).

    Args:
        re (str): The regular expression to be converted.

    Returns:
        DeterministicFiniteAutomaton: The deterministic finite automaton equivalent of the input regular expression.

    Raises:
        ValueError: If the input regular expression is not valid.

    Example:
        >>> regex_example = "abc|ab|a|c"
        >>> dfa_example = regex_to_dfa(regex_example)
    """

    epsilon_nfa = Regex(re).to_epsilon_nfa()
    _nfa = epsilon_nfa.to_deterministic()
    _dfa = _nfa.minimize()
    return _dfa


def graph_to_nfa(
    graph: MultiDiGraph, start_states_set: set[int], final_states_set: set[int]
) -> NondeterministicFiniteAutomaton:
    """
    Converts a NetworkX graph into a DeterministicFiniteAutomaton.

    Args:
        graph (networkx.MultiDiGraph): The NetworkX graph to be converted.
        start_states_set (): Start states
        final_states_set (): Final states
    Returns:
        NondeterministicFiniteAutomaton: The non-deterministic finite automaton equivalent of the input graph.

    Raises:
        ValueError: If the input graph is not a valid NetworkX graph.

    Example:
        >>> import networkx as nxx
        >>> G = nxx.DiGraph()
        >>> G.add_edge('A', 'B', label='a')
        >>> G.add_edge('B', 'C', label='b')
        >>> dfa_test = graph_to_nfa(G)
    """
    nfa = NondeterministicFiniteAutomaton()
    if len(start_states_set) == 0:
        for node in graph.nodes():
            nfa.add_start_state(node)
    for node in start_states_set:
        nfa.add_start_state(State(node))

    if len(final_states_set) == 0:
        for node in graph.nodes():
            nfa.add_final_state(node)
    for node in final_states_set:
        nfa.add_final_state(State(node))

    for u, v, label in graph.edges(data="label"):
        nfa.add_transition(u, label, v)

    return nfa


if __name__ == "__main__":
    import itertools
    import random

    regex_str = "(aa)*"
    regex = Regex(regex_str)
    regex_cfg = regex.to_cfg()
    regex_words = regex_cfg.get_words()
    if regex_cfg.is_finite():
        all_word_parts = list(regex_words)
        word_parts = random.choice(all_word_parts)
    else:
        index = random.randint(0, 2**9)
        word_parts = next(itertools.islice(regex_words, index, None))
        word = map(lambda x: x.value, word_parts)
        dfa = regex_to_dfa(regex_str)
        minimized_dfa = dfa.minimize()
        assert dfa.is_deterministic()
        assert dfa.is_equivalent_to(minimized_dfa)
        assert dfa.accepts(word)
