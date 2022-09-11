import filecmp
import os.path

from project.graph_utils import *

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_graph_save():
    graph = create_two_cycle_labeled_graph(
        size_of_first_cycle=42,
        size_of_second_cycle=29,
        edge_labels=("x", "y"),
    )
    save_graph(graph, os.sep.join([test_dir_path, "actual_graph.dot"]))
    assert filecmp.cmp(
        os.sep.join([test_dir_path, "actual_graph.dot"]),
        os.sep.join([test_dir_path, "expected_graph.dot"]),
    )
    os.remove(os.sep.join([test_dir_path, "actual_graph.dot"]))
