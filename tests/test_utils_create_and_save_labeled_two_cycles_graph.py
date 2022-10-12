from project import (
    create_and_save_labeled_two_cycles_graph,
    load_graph_from_dot,
    graph_to_nfa,
)
import filecmp
import os.path
from project.utils import save_graph_as_dot
from tests.test_graphs import all_test_graphs
import networkx as nx

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_42_13_formal_language():
    test_path = os.sep.join([test_dir_path, "test.dot"])
    exp_path = os.sep.join([test_dir_path, "expected.dot"])
    create_and_save_labeled_two_cycles_graph(42, 13, ("formal", "language"), test_path)
    assert filecmp.cmp(test_path, exp_path)
    os.remove(test_path)


def test_save_and_load_graph():
    for graph in all_test_graphs:
        save_graph_as_dot(graph.graph, "test_graph.dot")
        new_g = load_graph_from_dot("test_graph.dot")
        if nx.classes.is_empty(graph.graph):
            assert nx.classes.is_empty(new_g)
        else:
            assert graph_to_nfa(graph.graph).is_equivalent_to(graph_to_nfa(new_g))
