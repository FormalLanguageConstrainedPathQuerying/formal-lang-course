from project.dfa_utils import *
import networkx as nx
import pytest

reg_binary_mess_ended_by_zero = "(0|1)* 0"


def test_graph_to_nfa_nonexistent_start():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")
    with pytest.raises(Exception, match=".* start .*"):
        graph_to_nfa(graph, {42}, {0})
    with pytest.raises(Exception, match=".* final .*"):
        graph_to_nfa(graph, {0}, {42})


def test_graph_to_nfa_binary_mess_ended_by_zero():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")
    nfa = graph_to_nfa(graph, {0}, {1})
    assert nfa.is_equivalent_to(regex_str_to_dfa(reg_binary_mess_ended_by_zero))
