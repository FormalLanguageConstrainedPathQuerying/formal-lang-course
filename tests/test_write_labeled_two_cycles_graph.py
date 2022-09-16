import filecmp

from project.graph_utils import write_labeled_two_cycles_graph


def test_write_labeled_two_cycles_graph():
    write_labeled_two_cycles_graph(
        (3, 3), ("a", "b"), "tests/resources/task1/actual_graph.dot"
    )
    assert filecmp.cmp(
        "tests/resources/task1/actual_graph.dot",
        "tests/resources/task1/expected_graph.dot",
        shallow=False,
    )
