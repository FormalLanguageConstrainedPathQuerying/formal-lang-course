import filecmp

from project.utils.graph_utils import export_graph_to_dot, generate_labeled_two_cycles_graph


def test_():
    expected = generate_labeled_two_cycles_graph((3, 2), ("fst", "snd"))
    export_graph_to_dot(expected, "../tests/res/actual_graph.dot")

    assert filecmp.cmp("../tests/res/actual_graph.dot", "../tests/res/expected_graph.dot", shallow=False)
