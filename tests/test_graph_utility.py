import filecmp
import os
from cfpq_data import labeled_two_cycles_graph
from project.graph_utility.graph_utility import *


def test_create_graph_of_two_cycles():
    n = 5
    m = 3
    labels = ("a", "b")
    actual_graph = create_graph_of_two_cycles(
        first_cycle_nodes=n, second_cycle_nodes=m, labels=labels
    )
    expected_graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)

    assert expected_graph.nodes == actual_graph.nodes
    assert list(expected_graph.edges.data(data="label")) == list(
        actual_graph.edges.data(data="label")
    )


def test_save_graph_as_dot_empty_path():
    n = 3
    m = 3
    labels = ("a", "b")
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)
    save_graph_as_dot(graph=graph, output_name="test_result")

    assert filecmp.cmp(
        path.join(current_dir_path, "test_result.dot"),
        path.join(current_dir_path, "result", "sample.dot"),
    )

    os.remove(path.join(current_dir_path, "test_result.dot"))


def test_save_graph_as_dot_with_path():
    n = 3
    m = 3
    labels = ("a", "b")
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)
    save_graph_as_dot(
        graph=graph,
        output_name="test_result",
        output_path=path.join(current_dir_path, "result"),
    )

    assert filecmp.cmp(
        path.join(current_dir_path, "result", "test_result.dot"),
        path.join(current_dir_path, "result", "sample.dot"),
        shallow=False,
    )

    os.remove(path.join(current_dir_path, "result", "test_result.dot"))
