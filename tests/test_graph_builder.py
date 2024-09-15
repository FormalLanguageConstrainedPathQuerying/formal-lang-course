import filecmp
import cfpq_data
from project.hw1.graph_builder import Graph, load_graph, build_two_cycle_graph


def test_load_graph():
    graph_from_csv = cfpq_data.graph_from_csv("tests/travel/travel.csv")
    expected_edges_cnt = graph_from_csv.number_of_edges()
    expected_nodes_cnt = graph_from_csv.number_of_nodes()
    expected_labels = set(cfpq_data.get_sorted_labels(graph_from_csv))

    expected_graph = Graph(expected_edges_cnt, expected_nodes_cnt, expected_labels)
    actual = load_graph("travel")
    assert expected_graph == actual


def test_build_graph():
    build_two_cycle_graph(2, 2, ("a", "b"), "tests/actual.dot")
    assert filecmp.cmp("tests/actual.dot", "tests/expected.dot")
