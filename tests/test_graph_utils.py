import pytest
from pathlib import Path
from project.graph_utils import (
    load_graph_properties_by_name,
    make_labeled_two_cycles,
    GraphProperties,
)


@pytest.mark.parametrize(
    "graph_name, expected_node_count, expected_edge_count, expected_labels, should_fail",
    [
        ("bzip", 632, 556, {"d", "a"}, False),
        ("wc", 332, 269, {"d", "a"}, False),
        (
            "non_existent_graph",
            None,
            None,
            None,
            True,
        ),  # Error case: graph does not exist
    ],
)
def test_load_graph_properties_by_name(
    graph_name, expected_node_count, expected_edge_count, expected_labels, should_fail
):
    if should_fail:
        with pytest.raises(Exception):
            load_graph_properties_by_name(graph_name)
    else:
        expected_graph_properties = GraphProperties(
            node_count=expected_node_count,
            edge_count=expected_edge_count,
            labels=expected_labels,
        )
        actual_graph_properties = load_graph_properties_by_name(graph_name)
        assert actual_graph_properties == expected_graph_properties


@pytest.mark.parametrize(
    "first_cycle_size, second_cycle_size, labels, dot_file_path, should_fail",
    [
        (3, 4, ("a", "b"), Path("test_graph_1.dot"), False),  # Successful case
        (
            1,
            1,
            ("x", "y"),
            Path("test_graph_2.dot"),
            False,
        ),  # Successful case with minimal cycles
        (
            -1,
            4,
            ("a", "b"),
            Path("invalid_graph.dot"),
            True,
        ),  # Error case: negative cycle size
        (
            3,
            0,
            ("a", "b"),
            Path("invalid_graph.dot"),
            True,
        ),  # Error case: zero cycle size
    ],
)
def test_make_labeled_two_cycles(
    first_cycle_size, second_cycle_size, labels, dot_file_path, should_fail
):
    if should_fail:
        with pytest.raises(Exception):
            make_labeled_two_cycles(
                first_cycle_size, second_cycle_size, labels, dot_file_path
            )
    else:
        make_labeled_two_cycles(
            first_cycle_size, second_cycle_size, labels, dot_file_path
        )
        assert dot_file_path.exists()  # Check that the file was created

        # Verify the file content
        with open(dot_file_path, "r") as f:
            content = f.read()
            assert "digraph" in content  # Basic check that it's a graph
            assert labels[0] in content  # Check for the presence of labels in the file
            assert labels[1] in content

        dot_file_path.unlink()
