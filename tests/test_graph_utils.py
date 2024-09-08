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
