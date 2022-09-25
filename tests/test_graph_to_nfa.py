from project import *
from tests.test_graphs import *
import networkx as nx
import pytest

reg_binary_mess_ended_by_zero = "(0|1)* 0"


def test_graph_to_nfa_nonexistent_start():
    graph = binary_mess_ended_by_zero().graph
    with pytest.raises(Exception, match=".* start .*"):
        graph_to_nfa(graph, {42}, {0})
    with pytest.raises(Exception, match=".* final .*"):
        graph_to_nfa(graph, {0}, {42})


def test_graph_to_nfa_binary_mess_ended_by_zero():
    graph = binary_mess_ended_by_zero().graph
    nfa = graph_to_nfa(graph, {0}, {1})
    assert nfa.is_equivalent_to(regex_str_to_dfa(reg_binary_mess_ended_by_zero))
    for i in range(0, 42, 2):
        assert nfa.accepts("{0:b}".format(i))
        assert not nfa.accepts("{0:b}".format(i + 1))


def test_graph_to_nfa_ended_by_banana_ananas():
    graph = banana_ananas()
    nfa = graph_to_nfa(graph.graph, graph.start_states, graph.final_states)
    assert nfa.accepts("banana")
    assert nfa.accepts("ananas")
    assert nfa.accepts("mama_love_bananas")
    assert not nfa.accepts("banana_not_apple")
