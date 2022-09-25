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


def test_graph_to_nfa():
    for graph in all_test_graphs:
        nfa = graph_to_nfa(graph.graph, graph.start_states, graph.final_states)
        assert nfa.minimize().is_equivalent_to(
            regex_str_to_dfa(graph.reg)
        ), f'{graph.name} failed, not equal to "{graph.reg}"'
        acception_test(nfa, graph)
