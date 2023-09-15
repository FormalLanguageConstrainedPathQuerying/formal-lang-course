import os
import filecmp
import networkx as nx
from project import graph_utils


def test_get_graph_info():
    graph = graph_utils.get_graph_info("biomedical")

    assert graph[0] == 341
    assert graph[1] == 459
    assert graph[2] == {
        "subClassOf",
        "label",
        "type",
        "comment",
        "title",
        "language",
        "publisher",
        "description",
        "creator",
        "versionInfo",
    }


def test_save_two_cycles_graph_in_dot():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    expected_path = os.path.join(current_dir_path, "resources/expected.dot")
    actual_path = os.path.join(current_dir_path, "resources/actual.dot")

    graph_utils.save_two_cycles_graph_in_dot(10, 20, ("first", "second"), actual_path)

    assert filecmp.cmp(expected_path, actual_path, shallow=False)
