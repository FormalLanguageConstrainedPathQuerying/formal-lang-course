from project import graph_to_nfa
from test_graphs import binary_mess_ended_by_zero, all_test_graphs, acception_test
import pytest

reg_binary_mess_ended_by_zero = "(0|1)* 0"


def test_graph_to_nfa_nonexistent_start():
    graph = binary_mess_ended_by_zero().graph
    with pytest.raises(Exception, match=".* start .*"):
        graph_to_nfa(graph, {42}, {0})
    with pytest.raises(Exception, match=".* final .*"):
        graph_to_nfa(graph, {0}, {42})


def test_graph_to_nfa():
    for graph in all_test_graphs:
        nfa = graph_to_nfa(graph.graph, graph.start_states, graph.final_states)
        acception_test(nfa, graph)
