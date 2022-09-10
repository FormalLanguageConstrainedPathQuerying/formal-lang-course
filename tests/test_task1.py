from networkx import DiGraph, is_isomorphic
from networkx.drawing.nx_pydot import read_dot

from project.task1 import GraphData
from project.task1 import get_graph_data
from project.task1 import write_labeled_two_cycles_graph_to_dot


def test_get_graph_data():
    graph_name = "wc"
    expected_graph_data = GraphData(node_count=332, edge_count=269, labels={"A", "D"})
    actual_graph_data = get_graph_data(graph_name)
    assert actual_graph_data == expected_graph_data


def test_write_labeled_two_cycles_graph_to_dot(tmp_path):
    expected_graph = DiGraph(
        [
            (0, 1, dict(label="A")),
            (1, 0, dict(label="A")),
            (0, 2, dict(label="B")),
            (2, 3, dict(label="B")),
            (3, 0, dict(label="B")),
        ]
    )
    actual_path = tmp_path / "actual_graph.dot"
    write_labeled_two_cycles_graph_to_dot((1, 2), ("A", "B"), actual_path)
    actual_graph = DiGraph(read_dot(actual_path))
    assert is_isomorphic(
        actual_graph,
        expected_graph,
        edge_match=lambda e1, e2: e1["label"] == e2["label"],
    )
