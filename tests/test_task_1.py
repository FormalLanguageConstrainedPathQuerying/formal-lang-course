import filecmp
import os

from project import (
    create_labeled_two_cycles_graph,
    get_graph_params,
    save_to_dot
)


def test_get_graph_params():
    graph_params = get_graph_params("bzip")

    assert graph_params.node_count == 632
    assert graph_params.edge_count == 556
    assert graph_params.labels == {"d", "a"}


def test_save_cycled_graph():
    g = create_labeled_two_cycles_graph(
        (10, 10),
        ("first", "second"),
    )
    save_to_dot(g, "tests/data/output/task_1.dot")

    files_are_identical = filecmp.cmp(
        "tests/data/output/task_1.dot",
        "tests/data/example/task_1.dot",
    )

    assert files_are_identical


