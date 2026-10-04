from unittest.mock import Mock

import cfpq_data
import networkx as nx
import pydot
import pytest

from project.graph_utils import create_two_cycles_graph, get_graph_info


@pytest.mark.parametrize(
    "graph_name",
    [name for name in cfpq_data.DATASET if name in {"generations", "skos"}],
)
def test_get_graph_info_from_dataset(graph_name):
    """Compare statistics with independently parsed real dataset edges."""
    csv_path = cfpq_data.download(graph_name)
    vertices, labels = set(), set()
    edge_count = 0
    for line in csv_path.read_text(encoding="utf-8").splitlines():
        source, target, label = line.split()
        vertices.update((source, target))
        labels.add(label)
        edge_count += 1

    assert get_graph_info(graph_name) == (len(vertices), edge_count, labels)


def test_get_graph_info_with_common_node(tmp_path, monkeypatch):
    csv_path = tmp_path / "graph.csv"
    csv_path.write_text("0 1 a\n1 0 a\n0 2 b\n2 0 b\n", encoding="utf-8")
    monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_path))

    assert get_graph_info("example") == (3, 4, {"a", "b"})


def test_get_graph_info_without_common_node(tmp_path, monkeypatch):
    csv_path = tmp_path / "graph.csv"
    csv_path.write_text("0 1 a\n1 0 a\n2 3 b\n3 2 b\n", encoding="utf-8")
    monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_path))

    assert get_graph_info("example") == (4, 4, {"a", "b"})


def test_get_graph_info_unknown_graph():
    with pytest.raises(FileNotFoundError):
        get_graph_info("__missing_test_graph__")


def test_get_graph_info_empty_graph(tmp_path, monkeypatch):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")
    monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_path))

    assert get_graph_info("example") == (0, 0, set())


def test_get_graph_info_parallel_edges_and_self_loop(tmp_path, monkeypatch):
    csv_path = tmp_path / "graph.csv"
    csv_path.write_text("0 1 a\n0 1 a\n1 1 b\n", encoding="utf-8")
    monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_path))

    assert get_graph_info("example") == (2, 3, {"a", "b"})


def test_create_two_cycles_graph(tmp_path):
    graph = create_two_cycles_graph(2, 3, ("a", "b"), tmp_path / "graph.dot")

    assert graph.number_of_nodes() == 6
    assert graph.number_of_edges() == 7
    assert set(nx.get_edge_attributes(graph, "label").values()) == {"a", "b"}
    cycles = list(nx.simple_cycles(graph))
    assert len(cycles) == 2
    assert sorted(map(len, cycles)) == [3, 4]
    assert set(cycles[0]) & set(cycles[1]) == {0}


def test_create_two_cycles_saves_dot(tmp_path):
    output_path = str(tmp_path / "graph.dot")
    create_two_cycles_graph(1, 1, ("a", "b"), output_path)

    dot_graph = pydot.graph_from_dot_file(output_path)[0]
    assert dot_graph.get_type() == "digraph"
    assert {node.get_name() for node in dot_graph.get_nodes()} == {"0", "1", "2"}
    assert {
        (edge.get_source(), edge.get_destination(), edge.get_label())
        for edge in dot_graph.get_edges()
    } == {
        ("0", "1", "a"),
        ("1", "0", "a"),
        ("0", "2", "b"),
        ("2", "0", "b"),
    }


@pytest.mark.parametrize("n, m", [(0, 2), (2, 0), (-1, 2)])
def test_create_two_cycles_rejects_nonpositive_size(tmp_path, n, m):
    with pytest.raises(ValueError):
        create_two_cycles_graph(n, m, ("a", "b"), tmp_path / "graph.dot")


def test_create_two_cycles_requires_two_labels(tmp_path):
    with pytest.raises(ValueError):
        create_two_cycles_graph(2, 3, ("a",), tmp_path / "graph.dot")


def test_create_two_cycles_requires_integer_sizes(tmp_path):
    with pytest.raises(TypeError):
        create_two_cycles_graph(1.5, 2, ("a", "b"), tmp_path / "graph.dot")


@pytest.mark.parametrize("labels", ["ab", ("a", None)])
def test_create_two_cycles_rejects_invalid_label_types(tmp_path, labels):
    with pytest.raises(TypeError):
        create_two_cycles_graph(1, 1, labels, tmp_path / "graph.dot")


def test_create_two_cycles_with_same_labels(tmp_path):
    output_path = str(tmp_path / "graph.dot")
    graph = create_two_cycles_graph(1, 1, ("same", "same"), output_path)

    assert graph.number_of_edges() == 4
    assert set(nx.get_edge_attributes(graph, "label").values()) == {"same"}
    dot_graph = pydot.graph_from_dot_file(output_path)[0]
    assert len(dot_graph.get_edges()) == 4
    assert {edge.get_label() for edge in dot_graph.get_edges()} == {"same"}
