from networkx import MultiDiGraph
from pyformlang.finite_automaton import State
from project.dfa_nfa import (
    regex_to_dfa,
    graph_to_nfa,
)


def test_regex_to_dfa():
    regex = "a|b"
    dfa = regex_to_dfa(regex)

    assert dfa.accepts("a")
    assert dfa.accepts("b")

    assert not dfa.accepts("ab")
    assert not dfa.accepts("c")


def test_graph_to_nfa():
    graph = MultiDiGraph()
    graph.add_edges_from([(1, 2), (2, 3), (3, 1)])

    start_states = {1}
    final_states = {3}

    nfa = graph_to_nfa(graph, start_states, final_states)

    assert nfa.start_states == {State(1)}

    assert nfa.final_states == {State(3)}

    assert State(1) not in nfa.final_states
    assert State(2) not in nfa.final_states
