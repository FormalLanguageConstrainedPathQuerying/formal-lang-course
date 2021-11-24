import cfpq_data
import networkx as nx

from project.utils import graph_utils
from pathlib import Path


graph_env = {"test_graph": graph_utils.generate_two_cycles_graph("3", "4", "a", "b")}


def test_save_to_dot_path():
    path = graph_utils.save_to_dot(graph_env["test_graph"], "tests/data/test_graph.dot")
    assert path == Path("tests/data/test_graph.dot")


def test_graph_isomorphism(tmpdir):
    n, m = 52, 48
    edge_labels = ("a", "b")
    file = tmpdir.mkdir("test_dir").join("two_cycles.dot")

    graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )
    graph_utils.save_to_dot(graph, file)

    actual_graph_string = None
    with open(file, "r") as graph_file:
        actual_graph_string = graph_file.read()

    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )

    expected_graph_string = nx.drawing.nx_pydot.to_pydot(expected_graph).to_string()

    assert actual_graph_string == expected_graph_string
