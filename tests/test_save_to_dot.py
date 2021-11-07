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

    actual_graph = nx.drawing.nx_pydot.read_dot(file)
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )

    assert nx.is_isomorphic(actual_graph, expected_graph)
