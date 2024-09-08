import filecmp
import unittest
import cfpq_data
from project.hw1.graph_builder import Graph, load_graph, build_two_cycle_graph


def test_load_graph():
    graph_from_csv = cfpq_data.graph_from_csv("./travel/travel.csv")
    expected_edges_cnt = graph_from_csv.number_of_edges()
    expected_nodes_cnt = graph_from_csv.number_of_nodes()
    expected_labels = cfpq_data.get_sorted_labels(graph_from_csv)

    expected_graph = Graph(expected_edges_cnt, expected_nodes_cnt, expected_labels)
    actual = load_graph("travel")

    test_case = unittest.TestCase()
    test_case.assertEqual(expected_graph, actual)


def test_build_graph(tmp_path):
    build_two_cycle_graph(2, 2, ("a", "b"), tmp_path / "expected.dot")
    assert filecmp.cmp("tests/test1.dot", tmp_path / "expected.dot")
