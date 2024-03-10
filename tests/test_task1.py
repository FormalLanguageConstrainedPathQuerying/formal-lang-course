import pytest
from project.graph_helper import (
    get_graph_by_name,
    get_graph_info,
    export2_dot_file,
    build_graph_and_save_to_dot_file,
)
from networkx import MultiDiGraph
import networkx as nx


def test_get_graph_by_name():
    graph = get_graph_by_name("skos")
    assert isinstance(graph, MultiDiGraph)


def test_get_graph_info():
    graph = nx.MultiDiGraph()
    assert get_graph_info(graph)["nodes"] == 0
    assert get_graph_info(graph)["nodes"] == 0
    assert get_graph_info(graph)["edges"] == 0

    graph.add_edge(1, 2)
    assert get_graph_info(graph)["nodes"] == 2
    assert get_graph_info(graph)["edges"] == 1

    graph.add_edge(2, 3)
    assert get_graph_info(graph)["nodes"] == 3
    assert get_graph_info(graph)["edges"] == 2
    assert set(get_graph_info(graph)["nodes_list"]) == {1, 2, 3}
    assert set(get_graph_info(graph)["edges_list"]) == {(2, 3, 0), (1, 2, 0)}


def test_export2_dot_file(tmp_path):
    graph = nx.MultiDiGraph()
    graph.add_edge(1, 2)
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "graph.dot"
    export2_dot_file(graph, str(p))
    assert p.read_text() == "digraph  {\n1;\n2;\n1 -> 2  [key=0];\n}\n"


def test_build_graph_and_save_to_dot_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "graph.dot"
    graph = build_graph_and_save_to_dot_file([1, 2], ["a", "b"], str(p))
    assert isinstance(graph, MultiDiGraph)
    assert (
        p.read_text()
        == "digraph  {\n1;\n2;\n1 -> 2  [key=0, label=a];\n2 -> 1  [key=0, label=b];\n}\n"
    )
