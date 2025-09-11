import pytest

from project.utils import graph_info, two_cycles_graph


def test_graph_info():
    num_nodes, num_edges, labels = graph_info("wc")
    assert isinstance(num_nodes, int)
    assert isinstance(num_edges, int)
    assert isinstance(labels, set)


def test_create_two_cycles_graph(tmp_path):
    dot_file_path = tmp_path / "two_cycles.dot"
    two_cycles_graph(3, 4, ("a", "b"), str(dot_file_path))

    with open(dot_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "digraph" in content
    assert "a" in content or "b" in content


def test_two_cycles_graph_error(tmp_path):
    dot_file_path = tmp_path / "two_cycles.dot"
    with pytest.raises(ValueError, match="Нужно передать 2 метки для двух циклов."):
        two_cycles_graph(2, 3, ("a",), dot_file_path)
