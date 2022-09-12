import filecmp
import os.path

from project.graph_utils import *

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_graph_save():
    graph = build_two_cycle_labeled_graph(
        first_cycle_size=3,
        second_cycle_size=3,
        edge_labels=("A", "B"),
    )
    save_graph(graph, os.sep.join([test_dir_path, "actual_graph.dot"]))
    assert filecmp.cmp(
        os.sep.join([test_dir_path, "actual_graph.dot"]),
        os.sep.join([test_dir_path, "sample_graph.dot"]),
    )
    os.remove(os.sep.join([test_dir_path, "actual_graph.dot"]))
