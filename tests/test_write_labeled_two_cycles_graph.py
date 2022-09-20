import filecmp

from project.graph_utils import write_labeled_two_cycles_graph_as_dot


def test_write_labeled_two_cycles_graph():
    write_labeled_two_cycles_graph_as_dot(
        (3, 3),
        ("a", "b"),
        "tests/resources/test_write_labeled_two_cycles_graph/actual_graph.dot",
    )
    assert filecmp.cmp(
        "tests/resources/test_write_labeled_two_cycles_graph/actual_graph.dot",
        "tests/resources/test_write_labeled_two_cycles_graph/expected_graph.dot",
        shallow=False,
    )
