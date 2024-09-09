import pytest
import cfpq_data
import networkx
import pydot
from project.task1 import create_and_save_labeled_two_cycled_graph


def test_creating_and_saving():
    create_and_save_labeled_two_cycled_graph(
        3, 3, ("label3", "label33"), "saved_file.dot"
    )

    actual_graphs = pydot.graph_from_dot_file("saved_file.dot")

    if actual_graphs is None:
        pytest.fail("Expected not empty graph to load")

    load_graph = actual_graphs[0]
    nx_graph = networkx.drawing.nx_pydot.from_pydot(load_graph)

    assert nx_graph.number_of_nodes() == 7
    assert cfpq_data.get_sorted_labels(nx_graph) == ["label3", "label33"]
