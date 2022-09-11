import filecmp
import os

from project.graph_utils import *


def test_get_graph_info():
    graph = "pathways"
    graph_info = get_graph_info(graph)
    expected_graph_info = Graph(
        6238, 12363, labels={"imports", "narrower", "subClassOf", "type", "label"}
    )
    assert graph_info == expected_graph_info


def test_create_and_save_labeled_two_cycles_graph():
    create_two_cycles_graph_and_save_as_dot(
        (3, 3), ("A", "B"), "temp_for_create_two_cycles_graph.dot"
    )
    assert filecmp.cmp(
        "temp_for_create_two_cycles_graph.dot", "../tests/expected_graph_task1.dot"
    )
    os.remove("temp_for_create_two_cycles_graph.dot")
