from networkx import Graph, MultiDiGraph
from project.graph_info import (
    GraphInfo,
    get_graph_info,
    load_graph,
    create_and_save_dot,
)
from pathlib import Path
import filecmp


def test_get_graph_info_empty_graph():
    graph = Graph()

    expected_graph_info = GraphInfo()
    actual_graph_info = get_graph_info(graph)

    assert expected_graph_info == actual_graph_info


def test_get_graph_info_nonempty_graph():
    graph = MultiDiGraph()
    for i in range(10):
        graph.add_node(i)

    graph.add_edge(1, 3, label="a")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(4, 1, label="a")
    graph.add_edge(1, 4, label="c")
    graph.add_edge(1, 2, label="d")
    graph.add_edge(5, 6, label="e")
    graph.add_edge(4, 5, label="f")
    graph.add_edge(6, 7, label="g")
    graph.add_edge(7, 8, label="i")
    graph.add_edge(9, 10, label="k")
    graph.add_edge(8, 10, label="l")

    expected_graph_info = GraphInfo(
        number_of_nodes=10,
        number_of_edges=11,
        labels={"a", "b", "c", "d", "e", "f", "g", "i", "k", "l"},
    )
    actual_graph_info = get_graph_info(graph)

    assert expected_graph_info == actual_graph_info


def test_load_graph_bzip():
    actual_graph = load_graph("bzip")

    assert 632 == actual_graph.number_of_nodes()
    assert 556 == actual_graph.number_of_edges()


def test_save_graph_as_dot_file():

    graph = MultiDiGraph()
    for i in [1, 2, 3]:
        graph.add_node(i)
    graph.add_edge(1, 3, label="a")
    graph.add_edge(2, 3, label="b")

    curr_dir_path = Path(__file__).resolve().parent
    expected_file_path = curr_dir_path / "expected_graph_dot.dot"
    actual_file_path = curr_dir_path / "actual_graph_dot.dot"

    create_and_save_dot(graph, actual_file_path)
    assert filecmp.cmp(expected_file_path, actual_file_path, shallow=False)
